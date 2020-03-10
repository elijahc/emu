import os
import luigi
import re
import pandas as pd
import numpy as np
import scipy.io as sio
from ..pipeline.process import PDilTask
from ..pipeline.download import Raw, check_or_create, BehaviorRaw, ExperimentManifest,cache_fp
from ..utils import Experiment

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

class PDilCache(object):
    def __init__(self, patient_manifest='~/.emu/patient_manifest.csv'):
        self._pt_manifest_fp = os.path.expanduser(patient_manifest)
        exps = ExperimentManifest(study='pdil')
        if not exps.output().exists():
            luigi.build([exps],local_scheduler=True)

        with exps.output().open('r') as f:
            self.data_manifest = pd.read_csv(f)

    def load_behavior(self,patient_id=[1],include_practice=True):
        exp_files = self.data_manifest
        behavior_files = exp_files[exp_files.filename.isin(filter(lambda s: s.endswith('taskoutput.mat'),exp_files.filename))]
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