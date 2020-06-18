import pytest
import os
from emu.data_managers import Electrophysiology
from emu.pdil.raw import get_data_manifest

def test_init():
    data_manifest = get_data_manifest()

    dat = Electrophysiology(patient_id = 1, raw_files = data_manifest)
    print(dat)

    assert dat.patient_id == 1
    print('patient_id:\t',dat.patient_id)

    assert dat.seeg_raw_path == os.path.expanduser("~/.emu/pdil/pt_01/SEEG/raw")
    print('raw_path:\t:', dat.seeg_raw_path)
    
if __name__ == "__main__":
    data_manifest = get_data_manifest()

    dat = Electrophysiology(patient_id = 1, raw_files = data_manifest)
    print(dat)

