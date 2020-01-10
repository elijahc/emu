import luigi
import os
import numpy as np
import pandas as pd
from ..auth import jwt, DEFAULT_ROOT
from .utils import file_ids_by_channel
from .io import FileManifest

def check_or_create(dir_path):
    if dir_path == DEFAULT_ROOT:
        raise ValueError('cannot create root dir, please create {} yourself'.format(DEFAULT_ROOT))
    elif os.path.isfile(dir_path):
        raise ValueError('{} is a file'.format(dir_path))
    elif not os.path.exists(dir_path):
        # Make sure parent exists
        parent = os.path.split(dir_path)[0]
        if not os.path.exists(parent):
            check_or_create(parent)

        print('creating dir:\n{}'.format(dir_path))
        os.mkdir(dir_path)


class Patients(luigi.Task):
    file_id = luigi.Parameter(default=588757437066)
    data_root = os.path.expanduser('~/.emu')

    def run(self):
        client = jwt()
        fp = os.path.join(self.data_root,'patient_manifest.csv')
        with open(fp, 'wb') as open_file:
            client.file(self.file_id).download_to(open_file)
            open_file.close()

    def output(self):
        out_fp = os.path.join(self.data_root,'patient_manifest.csv')
        return luigi.LocalTarget(out_fp)

class Raw(luigi.Task):
    file_id = luigi.IntParameter()
    file_name = luigi.Parameter()
    save_to = luigi.Parameter(default=os.path.join(DEFAULT_ROOT,'pt_default'))
    overwrite = luigi.Parameter(default=False)

    def run(self):
        check_or_create(self.save_to)

        client = jwt()
        file = client.file(self.file_id)
        fp = os.path.join(self.save_to,self.file_name)

        with open(fp, 'wb') as open_file:
            file.download_to(open_file)
            open_file.close()

    def output(self):
        fp = os.path.join(self.save_to,self.file_name)
        return luigi.LocalTarget(fp)

class Channel(luigi.Task):
    patient_id = luigi.IntParameter()
    channel_id = luigi.IntParameter()
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))

    def load_ch_files(self):
        fm = FileManifest(data_root=self.data_root, patient_id=self.patient_id)
        fm_output = fm.output()
        with fm_output.open('r') as infile:
            files = pd.read_csv(infile,dtype={'filename':str,'type':str, 'id':np.int,'path':str})
        ch_files = file_ids_by_channel(files,channel_ids=[self.channel_id])
        return ch_files

    def requires(self):
        raw_dir = os.path.join(self.data_root,'pt{}'.format(self.patient_id),'sEEG/raw')
        ch_files = self.load_ch_files()
        fetch_channels = []
        for fid,fn in zip(ch_files.id.values,ch_files.filename.values):
            fetch_channels.append(Raw(file_id=fid,save_to=raw_dir,file_name=fn))
        return fetch_channels

    def run(self):
        pass

    def output(self):
        raw_dir = os.path.join(self.data_root,'pt{}'.format(self.patient_id),'sEEG/raw')
        ch_files = self.load_ch_files()
        out_files = [os.path.join(raw_dir,fn) for fn in ch_files.filename.values]
        out_targets = [luigi.LocalTarget(fp) for fp in out_files]
        return out_targets