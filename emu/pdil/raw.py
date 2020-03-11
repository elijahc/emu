import os
import luigi
import re
import pandas as pd
import numpy as np
import scipy.io as sio
import glob
from .. import neuralynx_io as nlx
from ..pipeline.process import PDilTask
from ..pipeline.download import Raw, check_or_create, BehaviorRaw, ExperimentManifest,cache_fp
from ..utils import Experiment

import logging

logger = logging.getLogger(__name__)

PAYOFF_DICT = {
    6: ('defect','copperate'),
    4: ('cooperate','cooperate'),
    2: ('defect','defect'),
    1: ('cooperate','defect')
}

def points_to_choice(pts):
    if pts in PAYOFF_DICT.keys():
        return PAYOFF_DICT[pts]
    else:
        raise ValueError('pts not in PAYOFF_DICT')
def label_blockstart(df,threshold=220000):
    labels = ['block_start']
    for i in np.arange(len(df.index.values))[1:-1]:
#         triplet = df.index.values[i-1:i+1]
        diff_prev = int(np.abs(df.index.values[i]-df.index.values[i-1]))
        diff_next = int(np.abs(df.index.values[i]-df.index.values[i+1]))
#         print([diff_prev, diff_next])
        if  diff_prev <= threshold or diff_next <= threshold:
            labels.append('block_start')
            j=1
#         elif i<len(df.index.values) and  <= threshold:
#             labels.append('block_start')
        else:
            labels.append('trial{}_start'.format(int(j)))
            j+=1
    labels.append('trial{}_start'.format(j))
    df['label'] = labels
    return df

def download_experiment(patient_id, data_root='~/.emu/',local_scheduler=True,include_practice=False):
    data_root = os.path.expanduser(data_root)
    exp = Experiment(study='pdil', patient_id=patient_id)
    exp_files = exp.files()
    print('filtering for files ending with taskoutput.mat')
    task_output_files = exp_files[exp_files.filename.isin(filter(lambda s: s.endswith('taskoutput.mat'),exp_files.filename))]
    print('downloading...')
    tasks = []
    for i,row in task_output_files.iterrows():
        if include_practice is False and row.filename.startswith('PRACTICE'):
            pass
        else:
            tasks.append(BehaviorRaw(patient_id=patient_id,file_id=row.id,file_name=row.filename))
    
    luigi.build(tasks,local_scheduler=local_scheduler)

    return [t.output().path for t in tasks]

def timestamps(filename,var_key='taskoutput'):
    dat = sio.loadmat(filename,squeeze_me=True)['taskoutput']
    
    df = pd.DataFrame.from_records({
        'reaction_time':dat['rxnTime_player1'].flat[0],
        'timing_wholesession':dat['timing_wholesession_trial_n'].flat[0],
        'timing_sumTictocs':dat['timing_sumTictocs_trial_n'].flat[0],
        'points':dat['playerA_pts_summary'].flat[0],
    })

    df['trial']=np.arange(len(df))+1

    if 'PRACTICE' in filename:
        df['block']=0
        df['opponent']=np.nan
        df['strategy']=np.nan

    else:
        rgx = re.compile(r"blockNum_(\d+)_(\w+)TT_(\w+)_taskoutput.mat")
        block,opp,strat = rgx.findall(filename)[0]
        df['block']=int(block)
        df['opponent']=opp
        df['strategy']=strat

    return df,dat

def extract_trial_timing(filename,struct_as_record=False):
    taskoutput = sio.loadmat(filename,squeeze_me=True,struct_as_record=struct_as_record)['taskoutput']
    timing = taskoutput.timing
    trial_keys = [
        'Time_scrn_flip_trials1',
        'Time_postscrn_flip_trials1',
        'Time_scrn_flip_trials2',
        'Time_postscrn_flip_trials2',
        'Time_scrn_flip_trials3',
        'Time_postscrn_flip_trials3',
        'Time_scrn_flip_trials4',
        'Time_postscrn_flip_trials4',
        'Time_scrn_flip_trials5',
        'Time_postscrn_flip_trials5',
    ]
    
    num_trials = len(getattr(timing,trial_keys[0]))
    logger.debug('Number of trials in block: {}'.format(num_trials))

    delta_t = [0]
    screen = [np.nan]
    events = ['trial_start']
    rd = [0]

    for i in np.arange(num_trials):
        ri = 0
        for t in trial_keys:
            ri+=1
            row = getattr(timing,t)
            delta_t.append(row[i:i+1].max())
            # records['round_idx'].append(ri)
            screen.append(t[-1])
            if 'postscrn' in t:
                events.append('keypress{}'.format(t[-1]))
            else:
                events.append('render_screen{}'.format(t[-1]))
    #         records['keypress'].append()
        rd.extend([i+1]*len(trial_keys))
        
    records = {
        'event_delta':delta_t,
        'trial':rd,
        'event':events,
        'screen':screen
    }

    df = pd.DataFrame.from_records(records).sort_values(['trial','screen'])    

    return df

class Game(luigi.Task):
    patient_id = luigi.IntParameter()
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))
    game_filename = luigi.Parameter(default='session.npy')
    save_to = luigi.Parameter(default=None)

    # def requires(self):
    #     return ExperimentManifest(data_root=self.data_root,patient_id=self.patient_id)

    def save_to_dir(self):
        if self.save_to is None:
            return os.path.join(
                cache_fp(self.data_root,'pdil',self.patient_id,'Behavior')
                )
        else:
            return self.save_to

    def requires(self):
        em = ExperimentManifest(data_root=self.data_root, patient_id=self.patient_id)
        # tasks = 

    def create(self):
        with self.input().open('r') as f:
            exp_files = pd.read_csv(f)

        task_output_files = exp_files[exp_files.filename.isin(filter(lambda s: s.endswith('taskoutput.mat'),exp_files.filename))]
        tasks = [BehaviorRaw(patient_id=self.patient_id,file_id=row.id, file_name=row.filename) for i,row in task_output_files.iterrows()]
        dfs = []
        for lt in self.input():
            df,_ = timestamps(lt.path)
            dfs.append(df)

        return pd.concat(dfs).sort_values(['block','trial']).reset_index().drop(columns=['index'])

    def run(self):
        out_fp = os.path.join(self.save_to_dir(),self.game_filename)
        out_df = self.create()
        out_df.to_pickle(out_fp)

    def output(self):
        out_fp = os.path.join(self.save_to_dir(),self.game_filename)
        return luigi.LocalTarget(out_fp)

class Electrophysiology(object):
    def __init__(self, patient_id, raw_path):
        self.patient_id = patient_id
        self.raw_path = raw_path

    def load_ncs(self):


    def load_all_nev(self):
        path = self.raw_path
        nev_files = sorted(glob.glob(os.path.join(path,'*.nev')))
        nev1 = nlx.load_nev(nev_files[0])['events']
        cols = nev1.dtype.names
        for p in nev_files:
            f = nlx.load_nev(p)['events']
            for row in f:
                r = {k:v for k,v in zip(cols,row)}
                r['path'] = os.path.split(p)[-1]
                yield r

    def events(self,index=None):
        nevs = self.load_all_nev()
        ev = pd.DataFrame.from_records(nevs,index=index)
        ev['EventString'] = [str(v,'utf-8') for v in ev.EventString.values]
        ev['time'] = pd.to_datetime(ev.TimeStamp.values,unit='us')
        ev = ev.set_index('TimeStamp')
        return ev

    def ttl(self):
        df = self.events()
        # Extract only events labeled ttl
        df = df[df.EventString=='ttl']

        # Add ttl labels
        df = label_blockstart(df)
        return df

class Participant(object):
    def __init__(self,patient_id, raw_files,seeg_raw_path=None):
        self.patient_id = patient_id
        self.all_files = raw_files
        self.behavior_files = self.all_files.query('type == "Behavior"')
        self.survey_files = self.all_files.query('type == "CSV"')

        self.behavior_raw_path = os.path.join(
            os.path.expanduser('~/.emu/'),
            'pdil',
            'pt_{:02d}'.format(self.patient_id),
            'Behavior',
            'raw') 

        if seeg_raw_path is not None:
            # self.seeg_raw_path = seeg_raw_path
            self.seeg = Electrophysiology(self.patient_id, seeg_raw_path)

    def cache_behavior(self):
        files = self.behavior_files

        tasks = []
        for i,row in self.behavior_files.iterrows():
            t = BehaviorRaw(
                patient_id=row.patient_id,
                file_id=row.id,
                file_name=row.filename,
                save_to=self.behavior_raw_path,
            )
            yield t

    def load_game_data(self):
        tasks = list(self.cache_behavior())
        luigi.build(tasks,local_scheduler=True)
        self.games = []
        for lt in tasks:
            df,_ = timestamps(lt.output().path)
            self.games.append(df)
            yield df

    def load_pdil_events(self):
        tasks = list(self.cache_behavior())
        self.pdil_events = []
        for t in tasks:
            if t.output().exists:
                timings = extract_trial_timing(t.output().path)
                self.pdil_events.append(timings)
                yield timings

        


class PDilCache(object):
    def __init__(self, patient_manifest='~/.emu/patient_manifest.csv'):
        self._pt_manifest_fp = os.path.expanduser(patient_manifest)
        exps = ExperimentManifest(study='pdil')
        if not exps.output().exists():
            luigi.build([exps],local_scheduler=True)

        with exps.output().open('r') as f:
            self.data_manifest = pd.read_csv(f).drop_duplicates()

    def load_behavior(self,patient_id=[1],include_practice=True):
        exp_files = self.data_manifest
        tasks = []
        for pt_id in patient_id:
            files = behavior_files.query('patient_id == {}'.format(pt_id))
            out_fp = os.path.join(
                os.path.expanduser('~/.emu/'),
                'pdil',
                'pt_{:02d}'.format(pt_id),
                'Behavior',
                'raw')

            tasks.extend([BehaviorRaw(
                patient_id=row.patient_id,
                file_id=row.id,
                file_name=row.filename,
                save_to=out_fp,
                ) for i,row in files.iterrows()])

        luigi.build(tasks,local_scheduler=True)

        dfs = []
        for lt in tasks:
            if not 'PRACTICE' in lt.output().path:
                df,_ = timestamps(lt.output().path)
                dfs.append(df) 
        
        return pd.concat(dfs).sort_values(['block','trial']).reset_index().drop(columns=['index'])