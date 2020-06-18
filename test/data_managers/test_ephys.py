import os
from emu.data_managers import Electrophysiology
from emu.pdil.raw import get_data_manifest

data_manifest = get_data_manifest()

dat = Electrophysiology(patient_id = 1, raw_files = data_manifest)
print(dat)

print('patient_id:\t',dat.patient_id)
print()

print('raw_path:\t:', dat.seeg_raw_path)

