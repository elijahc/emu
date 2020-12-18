import luigi
import os
import pandas as pd
import numpy as np
import scipy.signal as signal
from tqdm import tqdm
import warnings
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile, TimeSeries,NWBHDF5IO

from .download import FileManifest,Raw
from .remote import RemotePatientManifest
from .utils import file_ids_by_channel
from ..neuralynx_io import load_ncs

import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

def gen_ncs(fp_list,ignore_warnings=True):
    with warnings.catch_warnings():
        if ignore_warnings:
            warnings.simplefilter("ignore")

        for fp in fp_list:
            yield load_ncs(fp)

class PDilTask(luigi.Task):
    patient_id = luigi.IntParameter()
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))

    def patient_data(self):
        fm = RemotePatientManifest(patient_id=self.patient_id)

        with fm.output().open('r') as infile:
            manifest = pd.read_csv(infile,dtype={'filename':str,'type':str, 'id':np.int,'path':str})

        manifest = manifest.query('study == "pdil"')
        manifest = manifest.query('patient_id == {}'.format(self.patient_id))

        return manifest

class sEEGTask(luigi.Task):
    patient_id = luigi.IntParameter()
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))

    def ch_files(self,ch_ids):
        fm = FileManifest(patient_id=self.patient_id,data_root=self.data_root)
        if not os.path.exists(fm.output().path):
            fm.run()
        with fm.output().open('r') as infile:
            files = pd.read_csv(infile,dtype={'filename':str,'type':str, 'id':np.int,'path':str})
        ch_files = file_ids_by_channel(files,channel_ids=ch_ids)
        return ch_files

    def sEEG_root(self):
        path = os.path.join(self.data_root,'pt{}/sEEG'.format(self.patient_id))
        return path

class Downsample(sEEGTask):
    channel_id = luigi.IntParameter()
    decimate = luigi.IntParameter(default=4)

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
        files = [os.path.join(raw_dir,f) for f in files]

        ncs_timestamps = []
        ncs_data = []
        nlx_iter = gen_ncs(files)
        for ncs in tqdm(nlx_iter,total=len(files),desc='CH{}'.format(self.channel_id)):
            ncs_timestamps.append(signal.decimate(ncs['timestamp'],self.decimate))
            ncs_data.append(signal.decimate(ncs['data'],self.decimate).astype(np.float16))

        timestamp = np.concatenate(ncs_timestamps).astype(int)
        data = np.concatenate(ncs_data).astype(np.float16)

        ts_path = os.path.join(self.save_path(),'ts_{}'.format(self.channel_id))
        np.save(ts_path,timestamp)

        dat_path = os.path.join(self.save_path(),'CSC{}'.format(self.channel_id))
        np.save(dat_path, data)

    def output(self):
        ts_path = os.path.join(self.save_path(),'ts_{}'.format(self.channel_id))
        dat_path = os.path.join(self.save_path(),'CSC{}'.format(self.channel_id))
        outputs = [luigi.LocalTarget(fp+'.npy') for fp in [ts_path,dat_path]]

        return outputs

class NWB(sEEGTask):
    decimate = luigi.IntParameter(default=4)

    def save_path(self):
        return os.path.join(self.sEEG_root(),'data_1')

    def requires(self):
        self.channels = np.arange(20)+1
        downsampled = [Downsample(patient_id=self.patient_id,channel_id=ch,decimate=self.decimate) for ch in self.channels]
        req = {'timeseries':[],'data':[]}
        return downsampled

    def output(self):
        return luigi.LocalTarget(os.path.join(self.save_path(),'data.nwb'))

    def make_timeseries(self,ts_file,dat_file,ch):
        timestamps=np.load(ts_file.path)
        data=np.load(dat_file.path)
        ch_ts = TimeSeries(name='channel_{}'.format(ch),timestamps=timestamps/1000/1000,data=data,unit='uV')
        return ch_ts

    def run(self):
        ts_file,dat_file = self.input()[0]
        print(ts_file,ts_file.path)
        start_time = np.load(ts_file.path)[0]
        self.default_ts = self.make_timeseries(ts_file,dat_file,1)
        print(self.default_ts.timestamps)

        nwbfile = NWBFile(session_description='pt1 Neuralynx Data',
                          identifier='pt1',
                          session_start_time=datetime.fromtimestamp(start_time/1000/1000),
                          )

        nwbfile.add_acquisition(self.default_ts)
        i = 2
        for ts_out,dat_out in tqdm(self.input(),total=len(self.channels),desc='Creating Channels'):
            nts = np.load(ts_out.path)/1000/1000
            if np.all(nts==self.default_ts.timestamps):
                nts = self.default_ts

            dat = np.load(dat_out.path)
            ch_ts = TimeSeries(name='channel_{}'.format(i),timestamps=nts,data=dat, unit='uV',)
            nwbfile.add_acquisition(ch_ts)
            i+=1

        out_fp = os.path.join(self.save_path(),'data.nwb')
        with NWBHDF5IO(out_fp, 'w') as io:
            io.write(nwbfile)
