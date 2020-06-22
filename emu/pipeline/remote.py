import luigi
import os
import io
import numpy as np
import pandas as pd
from ..auth import jwt, DEFAULT_ROOT
from ..luigi.box import BoxTarget
from ..neuralynx_io import read_header, read_records, parse_header

class RemoteFile(luigi.ExternalTask):
    """
    Parameters
    ----------
    file_id : int
    file_path : str

    """
    file_id = luigi.IntParameter(default=None)
    file_path = luigi.Parameter(default=None) 

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

class RemoteNEV(RemoteFile):
    """
    Parameters
    ----------
    file_id : int
    file_path : str
    """
    file_id = luigi.IntParameter(default=None)
    file_path = luigi.Parameter(default=None)

    def load(self):
        with self.output().open('rb') as f:
            self.raw_header = read_header(f)
            # self.records = read_records(f, NEV_RECORD)
        return raw_header

class RemotePatientManifest(RemoteCSV):
    # file_id = luigi.IntParameter(default=DEFAULT_MANIFEST_FID)
    # patient_id = luigi.IntParameter()

    def output(self):
        return BoxTarget('/EMU/_patient_manifest.csv')

# For backwards compatibility
Patients = RemotePatientManifest