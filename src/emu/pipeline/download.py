import luigi
import os
import io
import numpy as np
import pandas as pd
from ..auth import jwt, DEFAULT_ROOT
from .utils import file_ids_by_channel
from ..utils import get_file_manifest,DEFAULT_MANIFEST_FID
from ..luigi.box import BoxTarget
from .remote import RemotePatientManifest

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

class FileManifest(luigi.Task):
    patient_id = luigi.IntParameter(default=1)
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))

    def requires(self):
        return PatientsLocal()

    def run(self):
        client = jwt()
        fp = os.path.join(self.data_root,'pt{}_manifest.csv'.format(self.patient_id))
        pt_str = self.input().open('r').read()
        with StringIO(pt_str) as infile:
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

class CacheData(luigi.Task):
    patient_id = luigi.IntParameter()
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu'))

    def requires(self):
        return PatientsLocal()

class CacheTaskOutput(CacheData):
    def run(self):
        client = jwt()
        with self.input().open('r') as infile:
            patient_manifest = pd.read_csv(infile)
        print(patient_manifest)

    def output(self):
        out_root = os.path.join(self.data_root,'pdil','pt_{}'.format(self.patient_id),'Behavior')
        self.input().path

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
    __name__ = 'Raw'
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))
    file_id = luigi.IntParameter(description='Box file_id')
    file_name = luigi.Parameter()
    save_to = luigi.OptionalParameter()
    overwrite = luigi.BoolParameter(default=False)

    def __repr__(self):
        cache = self.out_dir().split('.emu/')[-1]
        return '{}(file=/.emu/{}/{})'.format(self.__name__,cache,self.file_name)

    def out_dir(self):
        return self.save_to

    def download(self):
        client = jwt()
        file = client.file(self.file_id)
        fp = os.path.join(self.out_dir(),self.file_name)

        with open(fp, 'wb') as open_file:
            file.download_to(open_file)
            open_file.close()

    def run(self):
        check_or_create(self.out_dir())
        self.download()

    def output(self):
        out_fp = os.path.join(self.out_dir(),self.file_name)
        return luigi.LocalTarget(out_fp)

def cache_fp(data_root,study,patient_id,data_type=None):
    fp = os.path.join(
        data_root,
        study,
        'pt_{:04d}'.format(patient_id),
        )
    if data_type is not None:
        fp = os.path.join(fp,data_type)

    return os.path.expanduser(fp)

class BehaviorRaw(Raw):
    __name__ = 'BehaviorRaw'
    study = luigi.Parameter(default='pdil')
    patient_id = luigi.IntParameter()

    def cache_fp(self,data_type):
        return cache_fp(self.data_root,self.study,self.patient_id,data_type)

    def out_dir(self):
        return os.path.join(cache_fp(self.data_root,self.study,self.patient_id,'Behavior'),'raw')

class NLXRaw(Raw):
    __name__ = 'NLXRaw'
    study = luigi.Parameter(default='pdil')
    patient_id = luigi.IntParameter()

    def cache_fp(self,data_type):
        return cache_fp(self.data_root,self.study,self.patient_id,data_type)

    def out_dir(self):
        return os.path.join(self.cache_fp('SEEG'),'raw')

class ExperimentManifest(luigi.Task):
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))
    study = luigi.Parameter()
    # patient_id = luigi.IntParameter()
    file_name = luigi.Parameter(default='manifest.csv')

    def out_dir(self):
        return os.path.join(self.data_root,self.study)

    def requires(self):
        return RemotePatientManifest()

    def create(self):
        client = jwt()
        records = []
        with self.input().open('r') as f:
            patient_manifest = pd.read_csv(f)
        patient_folders = patient_manifest.query('patient_id > 0 & study == "{}"'.format(self.study))
        # patient_folders = patient_manifest.query('patient_id == {}'.format(self.patient_id))
        patient_ids = []
        for i,row in patient_folders.iterrows():
            fold = row.folder_id
            root = client.folder(fold)
            folder_files = list(get_file_manifest(root))
            
            records.extend(folder_files)
            patient_ids.extend([row.patient_id]*len(folder_files))
        files = pd.DataFrame.from_records(records)
        files['patient_id'] = patient_ids
        return files

    def run(self):
        check_or_create(self.out_dir())
        out = self.create()
        out.to_csv(os.path.join(self.out_dir(),self.file_name),index=False)

    def output(self):
        out_fp = os.path.join(self.out_dir(),self.file_name)
        return luigi.LocalTarget(out_fp) 