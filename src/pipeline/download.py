import luigi
import os
import io
import numpy as np
import pandas as pd
from ..auth import jwt, DEFAULT_ROOT
from .utils import file_ids_by_channel
from ..luigi.box import BoxTarget

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

class Patients(luigi.ExternalTask):
    file_id = luigi.IntParameter(default=588757437066)

    def output(self):
        return BoxTarget('/Doubt/patient_manifest.csv')

class FileManifest(luigi.Task):
    patient_id = luigi.IntParameter(default=1)
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))

    def requires(self):
        return Patients()

    def run(self):
        client = jwt()
        fp = os.path.join(self.data_root,'pt{}_manifest.csv'.format(self.patient_id))
        pt_str = self.input().open('r').read()
        with io.StringIO(pt_str) as infile:
            # print(infile)
            patients = pd.read_csv(infile,dtype={'patient_id':np.int,'folder_id':np.int,'start_date':str})
        print(patients)
        pt_rec = patients.query('patient_id == {}'.format(self.patient_id)).iloc[0]
        folder = client.folder(pt_rec.folder_id)
        file_recs = list(get_file_manifest(folder))
        files = pd.DataFrame.from_records(file_recs)
        files.to_csv(fp,index=False)

    def output(self):
        fp = os.path.expanduser('~/.emu/pt{}_manifest.csv'.format(self.patient_id))
        return luigi.LocalTarget(fp)

class PatientsLocal(luigi.Task):
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
        fm = FileManifest(patient_id=self.patient_id,data_root=self.data_root)
        if not os.path.exists(fm.output().path):
            fm.run()
        with fm.output().open('r') as infile:
            files = pd.read_csv(infile,dtype={'filename':str,'type':str, 'id':np.int,'path':str})
        ch_files = file_ids_by_channel(files,channel_ids=[self.channel_id])
        return ch_files

    def requires(self):
        return FileManifest(data_root=self.data_root, patient_id=self.patient_id)

    def run(self):
        raw_dir = os.path.join(self.data_root,'pt{}'.format(self.patient_id),'sEEG/raw')
        ch_files = self.load_ch_files()
        fetch_channels = []
        for fid,fn in zip(ch_files.id.values,ch_files.filename.values):
            yield Raw(file_id=fid,save_to=raw_dir,file_name=fn)

    def output(self):
        raw_dir = os.path.join(self.data_root,'pt{}'.format(self.patient_id),'sEEG/raw')
        ch_files = self.load_ch_files()
        out_files = [os.path.join(raw_dir,fn) for fn in ch_files.filename.values]
        out_targets = [luigi.LocalTarget(fp) for fp in out_files]
        return out_targets