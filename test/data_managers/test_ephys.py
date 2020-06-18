import pytest
import os
import warnings
import luigi
import pandas as pd
from pynwb import NWBFile, TimeSeries,NWBHDF5IO
from emu.data_managers import Electrophysiology
from emu.pdil.raw import get_data_manifest
import emu.neuralynx_io as nlx

def create_ephys():
    data_manifest = get_data_manifest()

    dat = Electrophysiology(patient_id = 1, raw_files = data_manifest)
    return dat

def create_nwb(ncs_paths,nev_fp,desc='test nwb file'):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ncs = nlx.load_ncs(ncs_paths.pop(0))
        nev = nlx.load_nev(nev_fp)

    uuid = nev['header']['SessionUUID']
    start_time = pd.to_datetime(ncs['time'][0],unit='us',utc=True).to_pydatetime()
    start_time_sec = start_time.timestamp()
    nwbfile = NWBFile(session_description=desc,
                      identifier=uuid,
                      session_start_time=start_time)

    return nwbfile

def test_add_to_nwb():
    ncs_tasks = [t for t in dat.cache_ncs() if 'PO_Day_02' in t.file_name and '0007' in t.file_name][:3]
    nev_tasks = [t for t in dat.cache_nev() if 'PO_Day_02' in t.file_name and '0007' in t.file_name][0]
    ncs_paths = [t.output().path for t in ncs_tasks]
    nwb = create_nwb(ncs_paths=ncs_paths,nev_fp=nev_tasks.output().path)

def test_init():
    dat = create_ephys()
    print(dat)

    assert dat.patient_id == 1
    print('patient_id:\t',dat.patient_id)

    assert dat.seeg_raw_path == os.path.expanduser("~/.emu/pdil/pt_01/SEEG/raw")
    print('raw_path:\t:', dat.seeg_raw_path)
    
if __name__ == "__main__":
    dat = create_ephys()

    print(dat)

    ncs_tasks = [t for t in dat.cache_ncs() if 'PO_Day_02' in t.file_name and '0007' in t.file_name][:3]
    nev_tasks = [t for t in dat.cache_nev() if 'PO_Day_02' in t.file_name and '0007' in t.file_name][0]

    luigi.build(tasks=ncs_tasks+[nev_tasks], local_scheduler=True)

    ncs_paths = [t.output().path for t in ncs_tasks]
    nwb = create_nwb(ncs_paths=ncs_paths,nev_fp=nev_tasks.output().path)
