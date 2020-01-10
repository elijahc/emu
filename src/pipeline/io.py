import os
import luigi
import io
import numpy as np
import pandas as pd
from ..auth import jwt, DEFAULT_ROOT
from ..utils import get_file_manifest, channel_fn_rgx
from boxsdk import DevelopmentClient
from .utils import file_ids_by_channel
from ..luigi.box import BoxTarget

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

class Timestamps(luigi.Task):
    patient_id = luigi.IntParameter(default=1)
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))

    def requires(self):
        return C

    def output(self):


if __name__ == "__main__":
    luigi.run()
