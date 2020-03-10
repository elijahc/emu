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
    file_id = luigi.IntParameter()
    file_name = luigi.Parameter()
    save_to = luigi.Parameter(default=os.path.join(DEFAULT_ROOT,'pt_default'))
    overwrite = luigi.BoolParameter(default=False)

    def save_to_dir(self,data_type='data_type'):
            if self.save_to is None:
                return os.path.join(
                    self.data_root,
                    self.study,
                    'pt_{:02d}'.format(self.patient_id),
                    data_type
                    )
            else:
                return self.save_to

    def download(self):
        client = jwt()
        file = client.file(self.file_id)
        fp = os.path.join(self.save_to_dir(),self.file_name)

        with open(fp, 'wb') as open_file:
            file.download_to(open_file)
            open_file.close()

    def run(self):
        out_dir = self.save_to_dir()
        check_or_create(out_dir)
        self.download()

    def output(self):
        out_fp = os.path.join(self.save_to_dir(),self.file_name)
        return luigi.LocalTarget(out_fp)