import os
import scipy.io as sio
import numpy as np
import re
import pandas as pd
from ..pipeline.download import BehaviorRaw
from ..pipeline.remote import RemoteCSV

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
    # logger.debug('Number of trials in block: {}'.format(num_trials))

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

class PDILBehavior(object):
    name = "pdil"

    def __init__(self,patient_id, raw_files, raw_path = None):
        self.patient_id = patient_id
        if raw_path is None:
            self.behavior_raw_path = os.path.join(
                os.path.expanduser('~/'),
                'pdil',
                'pt_{:02d}'.format(self.patient_id),
                'Behavior',
                'raw'
                )
        self.behavior_files = raw_files.query('type == "Behavior"')
    
    def __repr__(self):
        return "{}( n_files={} )".format(
            self.name,
            len(list(self.cache())),
            )

    def cache(self,verbose=False):
        """
        Yields
        ------
        luigi.Task
            Yields a BehaviorRaw task for downloading a single behavior file
        """
        for i,row in self.behavior_files.iterrows():
            t = BehaviorRaw(
                patient_id=row.patient_id,
                file_id=row.id,
                file_name=row.filename,
                save_to=self.behavior_raw_path,
            )
            yield t

    def files(self):
        """
        Returns
        ------
        files 
            Returns dataframe of this managers files
        """
        return self.behavior_files

    def load_game_data(self, local_scheduler=False):
        tasks = list(self.cache())
        missing_tasks = [t for t in tasks if not t.output().exists()]
        print('{} missing tasks'.format(len(missing_tasks)))

        if len(missing_tasks) > 0:
            luigi.build(missing_tasks,local_scheduler=local_scheduler)

        for lt in tasks:
            df,_ = timestamps(lt.output().path)
            yield df

    def add_to_nwb(self, nwb, blocks=[0,1,2]):
        """
        Returns
        ------
        nwb 
            Returns an nwb modified to include PDILBehavior data in the trial column named "outcome"
        """
        outcomes = pd.concat(self.load_game_data())
        outcomes = outcomes[outcomes.block.isin(blocks)]
        trial_delta = outcomes.sort_values(['block','trial']).timing_sumTictocs.values
        choices = pd.DataFrame.from_records(map(points_to_choice,outcomes.points.values),columns=['A','B'])
        choices['points'] = outcomes.points.values
        choices['tuple'] = [a[0].upper()+'-'+b[0].upper() for a,b in zip(choices.A.values,choices.B.values)]

        nwb.add_trial_column(name='outcome',description='Choice pair for both players')

        return nwb