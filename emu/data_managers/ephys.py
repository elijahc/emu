import io
import os
import luigi
import re
import numpy as np
import glob
import warnings
import pandas as pd
from ..pipeline.download import NLXRaw
from ..pipeline.remote import RemoteCSV
from ..neuralynx_io import load_nev, nev_as_records, load_ncs, nev_as_dataframe
from ..nwb import ncs_to_nwb

class Electrophysiology(object):
    name = "seeg"

    def __init__(self, patient_id, raw_files, raw_path=None):
        self.patient_id = patient_id
        if raw_path is not None:
            self.seeg_raw_path = raw_path
        else:
            self.seeg_raw_path = os.path.join(
                os.path.expanduser('~/.emu'),
                'pdil',
                'pt_{:02d}'.format(self.patient_id),
                'SEEG',
                'raw'
                )

        self.seeg_files = raw_files.query('type == "SEEG"')

        self.electrode_locations = None
        if 'electrode_locations.csv' in self.seeg_files.filename.values:
            loc = self.seeg_files[self.seeg_files.filename.isin(['electrode_locations.csv'])].iloc[0]
            self.electrode_locations = RemoteCSV(file_id=loc.id).load()

    def files(self):
        return self.seeg_files

    def __repr__(self):
        return "{}(n_ncs_files={}, n_nev_files={})".format(
            self.name,
            len(list(self.cache_ncs())),
            len(list(self.cache_nev()))
            )

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
                    save_to=self.seeg_raw_path,
                )
                yield t

    def cache_nev(self,verbose=False):
        """
        Yields
        ------
        luigi.Task
            Yields all NLXRaw luigi tasks for downloading a nev files from box
        """
        for i,row in self.seeg_files.iterrows():
            if row.filename.endswith('.nev'):
                t = NLXRaw(
                    patient_id = row.patient_id,
                    file_id = row.id,
                    file_name=row.folder+'.'+row.filename,
                    save_to=self.seeg_raw_path,
                )
                yield t

    def cache(self):
        for t in self.cache_nev():
            yield t
        
        for t in self.cache_ncs():
            yield t

    def gen_nlx_chunks(self):
        for c in self.chunks:
            nev_file = os.path.join(self.seeg_raw_path,'Events_{}.nev'.format(c))
            ncs_files = sorted(glob.glob(os.path.join(self.seeg_raw_path,'*{}.ncs'.format(c))))

            yield nev_file,ncs_files

    def events(self,index='TimeStamp'):
        nev_files = sorted(glob.glob(os.path.join(self.seeg_raw_path,'*.nev')))
        nev_dataframes = [nev_as_dataframe(fp) for fp in nev_files]
        ev = pd.concat(nev_dataframes)

        return ev

    def ttl(self):
        df = self.events()
        # Extract only events labeled ttl
        df = df[df.EventString=='ttl']

        # Add ttl labels
        df = label_blockstart(df)
        return df