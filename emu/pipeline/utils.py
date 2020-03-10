import os
import luigi
import pandas as pd
import numpy as np
import scipy.io as sio
from ..auth import jwt
from ..utils import get_file_manifest, _get_ch
from ..luigi.box import BoxTarget

def file_ids_by_channel(file_manifest, channel_ids=[16]):
    channels = file_manifest[file_manifest.type=="Channel"].copy()
    channels['ch'] = list(map(_get_ch, channels.filename.values))

    return channels[channels.ch.isin(channel_ids)]

class TaskOutput(object):
    def __init__(self,filepath,struct_name='taskoutput',squeeze=True):
        self.filepath = filepath
        self.struct_name = struct_name
        
        self._data = sio.loadmat(self.filepath,squeeze_me=squeeze)[self.struct_name]
        for k in ['playerA_pts_summary','rxnTime_player1','timing_wholesession_trial_n']:
            setattr(self,k,self._data[k].flat[0])

        for i in np.arange(2)+1:
            k = 'choice_matrix_player'+str(i)
            setattr(self,k,self._data[k].flat[0][0][-1])

        self.timing = self._data['timing']
    
    def keys(self):
        return self._data.dtype.names