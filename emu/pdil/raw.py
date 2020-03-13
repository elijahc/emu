import os
import luigi
import re
import pandas as pd
import numpy as np
import scipy.io as sio
import glob
import warnings
from .. import neuralynx_io as nlx
from ..pipeline.process import PDilTask
from ..pipeline.download import Raw, check_or_create, BehaviorRaw, ExperimentManifest,cache_fp,NLXRaw
from ..utils import Experiment
from ..neuralynx_io import nev_as_records
from ..nwb import nlx_to_nwb

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

def taskoutput_meta(filename, rgx_string=r"blockNum_(\d+)_(\w+)TT_(\w+)_taskoutput.mat"):
    if 'PRACTICE' in filename:
        block=0
        opp = np.nan
        strat = np.nan
    else:
        rgx = re.compile(rgx_string)
        block,opp,strat = rgx.findall(filename)[0]

    return int(block),opp,strat

def timestamps(filename,var_key='taskoutput'):
    dat = sio.loadmat(filename,squeeze_me=True)['taskoutput']
    

    df = pd.DataFrame.from_records({
        'reaction_time':dat['rxnTime_player1'].flat[0],
        'timing_wholesession':dat['timing_wholesession_trial_n'].flat[0],
        'timing_sumTictocs':dat['timing_sumTictocs_trial_n'].flat[0],
        'points':dat['playerA_pts_summary'].flat[0],
    })

    df['trial']=np.arange(len(df))+1

    block,opp,strat = taskoutput_meta(filename)
    df['block']=block
    df['opponent']=opp
    df['strategy'] = strat

    return df,dat

def extract_trial_timing(filename,struct_as_record=False):
    block,opp,strat = taskoutput_meta(filename)

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
        'screen':screen,
    }

    df = pd.DataFrame.from_records(records).sort_values(['trial','screen'])    
    df['block']=block

    return df

class Electrophysiology(object):
    def __init__(self, patient_id, box_files, raw_path=None):
        self.patient_id = patient_id
        if raw_path is not None:
            self.raw_path = raw_path

        self.seeg_files = box_files.query('type == "SEEG"')
        # ncs_files = sorted(glob.glob(os.path.join(raw_path,'*.ncs')))
        self.chunks = sorted(np.unique(np.array([f[-8:-4] for f in self.seeg_files])))

    def gen_nlx_chunks(self):
        for c in self.chunks:
            nev_file = os.path.join(self.raw_path,'Events_{}.nev'.format(c))
            ncs_files = sorted(glob.glob(os.path.join(self.raw_path,'*{}.ncs'.format(c))))

            yield nev_file,ncs_files

    def load_all_nev(self):
        path = self.raw_path
        nev_files = sorted(glob.glob(os.path.join(path,'*.nev')))
        for p in nev_files:
            f = nlx.load_nev(p)
            if len(f) > 0:
                yield list(nev_as_records(f))

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
        self.seeg_files = self.all_files.query('type == "SEEG"')

        self.behavior_raw_path = os.path.join(
            os.path.expanduser('~/.emu/'),
            'pdil',
            'pt_{:02d}'.format(self.patient_id),
            'Behavior',
            'raw') 

        if seeg_raw_path is not None:
            # self.seeg_raw_path = seeg_raw_path
            self.seeg = Electrophysiology(self.patient_id, 
                box_files=self.seeg_files, raw_path = seeg_raw_path)

    def cache_behavior(self,verbose=False):
        for i,row in self.behavior_files.iterrows():
            t = BehaviorRaw(
                patient_id=row.patient_id,
                file_id=row.id,
                file_name=row.filename,
                save_to=self.behavior_raw_path,
            )
            yield t

    def cache_nev(self,verbose=False):
        for i,row in self.seeg_files.iterrows():
            if row.filename.endswith('.nev'):
                t = NLXRaw(
                    patient_id = row.patient_id,
                    file_id = row.id,
                    file_name=row.folder+'.'+row.filename,
                    save_to=self.seeg.raw_path,
                )
                yield t

    def cache_ncs(self, verbose=False):
        for i,row in self.seeg_files.iterrows():
            if row.filename.endswith('.ncs'):
                t = NLXRaw(
                    patient_id = row.patient_id,
                    file_id = row.id,
                    file_name=row.folder+'.'+row.filename,
                    save_to=self.seeg.raw_path,
                )
                yield t

    def load_game_data(self, local_scheduler=False):
        tasks = list(self.cache_behavior())
        missing_tasks = [t for t in tasks if not t.output().exists()]
        print('{} missing tasks'.format(len(missing_tasks)))

        if len(missing_tasks) > 0:
            luigi.build(missing_tasks,local_scheduler=local_scheduler)

        for lt in tasks:
            df,_ = timestamps(lt.output().path)
            yield df

    def load_pdil_events(self,local_scheduler=False):
        tasks = list(self.cache_behavior())
        missing_tasks = [t for t in tasks if not t.output().exists()]
        print('{} missing tasks'.format(len(missing_tasks)))

        if len(missing_tasks) > 0:
            luigi.build(missing_tasks,local_scheduler=local_scheduler)

        for t in tasks:
            if t.output().exists:
                timings = extract_trial_timing(t.output().path)

                timings['ttl_delta'] = timings.event_delta.cumsum()

                yield timings

    def create_nwb(self,nev_fp,ncs_fps,blocks, desc=''):
        self.nwb = nlx_to_nwb(nev_fp,ncs_fps,desc)
        ttl = self.nwb.acquisition['ttl']
        trial_starts = [t for d,t in zip(ttl.data,ttl.timestamps) if d.startswith('trial')]

        # Calculate Trial deltas
        pdil_events = pd.concat(self.load_pdil_events())
        pdil_events = pdil_events[pdil_events.block.isin(blocks)]

        outcomes = pd.concat(self.load_game_data())
        outcomes = outcomes[outcomes.block.isin(blocks)]
        trial_delta = outcomes.sort_values(['block','trial']).timing_sumTictocs.values
        choices = pd.DataFrame.from_records(map(points_to_choice,outcomes.points.values),columns=['A','B'])
        choices['points'] = outcomes.points.values
        choices['tuple'] = [a[0].upper()+'-'+b[0].upper() for a,b in zip(choices.A.values,choices.B.values)]

        self.nwb.add_trial_column(name='outcome',description='Choice pair for both players')
        for start,dt,choice in zip(trial_starts,trial_delta,choices.tuple.values):

            self.nwb.add_trial(start_time=start,stop_time=start+dt,outcome=choice)

        return self.nwb

def get_data_manifest(study='pdil'):
    exps = ExperimentManifest(study='pdil')
    if not exps.output().exists():
        luigi.build([exps],local_scheduler=True)

    with exps.output().open('r') as f:
        return pd.read_csv(f).drop_duplicates()