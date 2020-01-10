import luigi
import os
import pandas as pd
import numpy as np
import src.neuralynx_io
import scipy.signal as signal
from tqdm import tqdm
import warnings

from .download import FileManifest,Raw
from .utils import file_ids_by_channel
from ..neuralynx_io import load_ncs

def gen_load_timestamps(fp_list,raw_root,downsample=4,ignore_warnings=True):
    with warnings.catch_warnings():
        if ignore_warnings:
            warnings.simplefilter("ignore")

        for fp in fp_list:
            ncs = load_ncs(os.path.join(raw_root,fp))
            yield signal.decimate(ncs['timestamp'],q=downsample)

class ChannelTimestamp(luigi.Task):
    patient_id = luigi.IntParameter()
    channel_id = luigi.IntParameter()
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))

    def load_ch_files(self):
        fm = FileManifest(patient_id=self.patient_id,data_root=self.data_root)
        if not os.path.exists(fm.output().path):
            fm.run()
        with fm.output().open('r') as infile:
            files = pd.read_csv(infile,dtype={'filename':str,'type':str, 'id':np.int,'path':str})
        ch_files = file_ids_by_channel(files,channel_ids=[self.channel_id])
        return ch_files

    def save_path(self):
        save_path = os.path.join(self.data_root,'pt{}/sEEG/data_1'.format(self.patient_id))
        return save_path

    def requires(self):
        raw_dir = os.path.join(self.data_root,'pt{}'.format(self.patient_id),'sEEG/raw')
        ch_files = self.load_ch_files()
        fetch_channels = []
        for fid,fn in zip(ch_files.id.values,ch_files.filename.values):
            fetch_channels.append(Raw(file_id=fid, save_to=raw_dir, file_name=fn))
        return fetch_channels

    def run(self):
        files = [f.path for f in self.input()]
        files = sorted(files)
        raw_dir = os.path.join(self.data_root,'pt{}'.format(self.patient_id),'sEEG/raw')

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


