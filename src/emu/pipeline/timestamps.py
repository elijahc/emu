import luigi
import os
import pandas as pd
import numpy as np
import scipy.signal as signal
from tqdm import tqdm
import warnings

from .download import FileManifest,Raw
from .utils import file_ids_by_channel
from ..neuralynx_io import load_ncs
from .process import sEEGTask

class ChannelTimestamp(sEEGTask):
    channel_id = luigi.IntParameter()

    def save_path(self):
        return os.path.join(self.sEEG_root(),'data_1')

    def requires(self):
        raw_dir = os.path.join(self.sEEG_root(),'raw')
        ch_files = self.ch_files([self.channel_id])
        fetch_channels = []
        for fid,fn in zip(ch_files.id.values,ch_files.filename.values):
            fetch_channels.append(Raw(file_id=fid, save_to=raw_dir, file_name=fn))
        return fetch_channels

    def run(self):
        files = [f.path for f in self.input()]
        files = sorted(files)
        raw_dir = os.path.join(self.sEEG_root(),'raw')

        ncs_timestamps = []
        t_iter = gen_load_timestamps(files,raw_dir,4)
        for ts in tqdm(t_iter,total=len(files),desc='CH{}'.format(self.channel_id)):
            ncs_timestamps.append(ts)

        timestamp = np.concatenate(ncs_timestamps).astype(int)

        out_path = os.path.join(self.save_path(),'timestamp_{}'.format(self.channel_id))
        np.save(out_path,timestamp)

    def output(self):
        t_dir = self.save_path()
        return luigi.LocalTarget(os.path.join(t_dir,'timestamp_{}'.format(self.channel_id)))
