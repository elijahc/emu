import os
import luigi
import pandas as pd
from ..auth import jwt
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
    data_root = luigi.IntParameter(default=os.path.expanduser('~/.emu/'))

    def requires(self):
        return Patients()

    def run(self):
        client = jwt()
        fp = os.path.join(self.data_root,'pt{}_manifest.csv'.format(self.patient_id))
        with self.input().open('r') as infile:
            patients = pd.read_csv(infile)
            folder_id = patients.query('patient_id == {}'.format(self.patient_id)).iloc[0].folder_id
            folder = client.folder(folder_id)
            file_recs = list(get_file_manifest(folder))
            files = pd.DataFrame.from_records(file_recs)
            files.to_csv(fp,index=False)

    def output(self):
        fp = os.path.expanduser('~/.emu/pt{}_manifest.csv'.format(self.patient_id))
        return luigi.LocalTarget(fp)

if __name__ == "__main__":
    luigi.run()
