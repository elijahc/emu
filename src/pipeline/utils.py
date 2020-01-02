import os
import luigi
import pandas as pd
from ..auth import jwt
from ..utils import get_file_manifest

class FileManifest(luigi.Task):
    patient_id = luigi.Parameter(default=1)
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))

    def requires(self):
        return Patients(self.data_root)

    def run(self):
        client = jwt()
        fp = os.path.join(self.data_root,'pt{}_manifest.csv'.format(self.patient_id))
        with self.input().open('r') as infile:
            patients = pd.read_csv(infile)
            folder_id = patients.query('patient_id == {}'.format(self.patient_id)).iloc[0].folder_id
            folder = client.folder(folder_id)
            file_recs = list(get_file_manifest(folder))
            files = pd.DataFrame.from_records(file_recs)
            files.to_csv(fp)

    def output(self):
        fp = os.path.expanduser('~/.emu/pt{}_manifest.csv'.format(self.patient_id))
        return luigi.LocalTarget(fp)

class Patients(luigi.Task):
    file_id = luigi.Parameter(default=588757437066)
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))

    def run(self):
        client = jwt()
        fp = os.path.join(self.data_root,'patient_manifest.csv')
        with open(fp, 'wb') as open_file:
            client.file(self.file_id).download_to(open_file)
            open_file.close()

    def output(self):
        out_fp = os.path.join(self.data_root,'patient_manifest.csv')
        return luigi.LocalTarget(out_fp)

class Channel(luigi.Task):
    patient_id = luigi.Parameter()
    channel_id = luigi.Parameter()
    raw_dir = luigi.Parameter(default=os.path.expanduser('~/.emu/raw'))
    data_dir = luigi.Parameter(default=os.path.expanduser('~/.emu/raw'))

    # def requires(self):
    #     output = {
    #         'patients':Patients(),
    #         'file_manifest',
    #     }
    #     return output
