import luigi
import os
import io
import numpy as np
import pandas as pd
from ..auth import jwt, DEFAULT_ROOT
from ..luigi.box import BoxTarget
from ..utils import is_url,generate_id, md5_16,get_file_manifest
from ..neuralynx_io import read_header, read_records, parse_header

class RemoteFile(luigi.ExternalTask):
    """
    Parameters
    ----------
    file_id : int
    file_path : str

    """
    file_id = luigi.IntParameter(default=None)
    file_path = luigi.OptionalParameter(default=None) 

    def output(self):
        if self.file_id is None and self.file_path is None:
            raise ValueError('file_id or file_path must be provided')
        elif self.file_id is not None:
            return BoxTarget(file_id=self.file_id)
        else:
            return BoxTarget(path=self.file_path)

class RemoteCSV(RemoteFile):
    """
    Parameters
    ----------
    file_id : int
    file_path : str
    """
    file_id = luigi.IntParameter(default=None)
    file_path = luigi.OptionalParameter(default=None)

    def load(self, parse_func=pd.read_csv,force=False):
        """
        Parameters
        ----------
        parse_func : func
            Default is pd.read_csv

        force : bool
            Force a reload from the server, Default is False
        """
        if force or not hasattr(self,'content'):
            with self.output().open('r') as f:
                self.content = parse_func(f)

        return self.content

class RemoteNLX(RemoteFile):
    """
    Parameters
    ----------
    file_id : int
    file_path : str
    """
    file_id = luigi.IntParameter()
    # file_path = luigi.Parameter(default=None)

    def raw_header(self):
        with self.output().open('rb') as f:
            self.raw_header = read_header(f)
        return raw_header

    def header(self):
        return parse_header(self.raw_header())

class RemotePatientManifest(RemoteCSV):
    # file_id = luigi.IntParameter(default=DEFAULT_MANIFEST_FID)
    # patient_id = luigi.IntParameter()

    def output(self):
        return BoxTarget('/EMU/_patient_manifest.csv')

    def register_new_data(self,firstname,lastname,study,data_type,folder_id=None,path=None):
        if not self.output().exists():
            raise ValueError(self.output().path+' does not exist')
        elif folder_id is None and path is None:
            raise ValueError('Must provide either folder_id, url, or valid box path')

        if folder_id is None and is_url(path):
            _,_,domain,resource,fid = path.split('/')
            if domain != 'app.box.com' or resource != 'folder':
                raise ValueError('url must be a Box.com folder url https://app.box.com/folder/00000000')
            path_fid = int(fid)
        
        folder_id = folder_id or path_fid
        
        pt_id = generate_id(firstname,lastname)
        
        return pt_id,firstname.upper()[0]+lastname.upper()[0],study,data_type,folder_id
        # folder_id = folder_id or 


class RemoteStudyManifest(RemoteCSV):
    study = luigi.Parameter()

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

    def output(self):
        return BoxTarget('/EMU/STUDY_{}/manifest.csv'.format(self.study.upper()))

# For backwards compatibility
Patients = RemotePatientManifest