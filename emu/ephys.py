import io
import luigi
import re
import numpy as np
import glob
import warnings
import pandas as pd
from .pipeline.download import NLXRaw

class Electrophysiology(object):
    def __init__(self, patient_id, box_files, raw_path=None):
        self.patient_id = patient_id
        if raw_path is not None:
            self.raw_path = raw_path

        self.seeg_files = box_files.query('type == "SEEG"')
        # ncs_files = sorted(glob.glob(os.path.join(raw_path,'*.ncs')))
        self.chunks = sorted(np.unique(np.array([f[-8:-4] for f in self.seeg_files])))

    def gen_nlx_chunks(self):
        for c in self.chunks:
            nev_file = os.path.join(self.raw_path,'Events_{}.nev'.format(c))
            ncs_files = sorted(glob.glob(os.path.join(self.raw_path,'*{}.ncs'.format(c))))

            yield nev_file,ncs_files

    def load_all_nev(self):
        path = self.raw_path
        nev_files = sorted(glob.glob(os.path.join(path,'*.nev')))
        for p in nev_files:
            f = nlx.load_nev(p)
            if len(f) > 0:
                yield list(nev_as_records(f))

    def events(self,index=None):
        nevs = self.load_all_nev()
        ev = pd.DataFrame.from_records(nevs,index=index)
        ev['EventString'] = [str(v,'utf-8') for v in ev.EventString.values]
        ev['time'] = pd.to_datetime(ev.TimeStamp.values,unit='us')
        ev = ev.set_index('TimeStamp')
        return ev

    def ttl(self):
        df = self.events()
        # Extract only events labeled ttl
        df = df[df.EventString=='ttl']

        # Add ttl labels
        df = label_blockstart(df)
        return df

    def cache(self):
        pass

    def cache_ncs(self):
        """
        Yields
        ------
        luigi.Task
            Yields a NLXRaw task for downloading a single ncs file from box
        """
        for i,row in self.seeg_files.iterrows():
            if row.filename.endswith('.ncs'):
                t = NLXRaw(
                    patient_id = row.patient_id,
                    file_id = row.id,
                    file_name=row.folder+'.'+row.filename,
                    save_to=self.seeg.raw_path,
                )
                yield t
        pass

    def cache_nev(self):
        pass
