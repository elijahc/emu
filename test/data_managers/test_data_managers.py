import os
from emu.data_managers import PDILBehavior,Participant,Electrophysiology
from emu.pdil.raw import get_data_manifest


data_manifest = get_data_manifest()

pdil = PDILBehavior(patient_id = 1, raw_files = data_manifest)
seeg = Electrophysiology(patient_id = 1, raw_files = data_manifest)



p1 = Participant(patient_id = 1, raw_files=data_manifest, results=[
    pdil,
    seeg,]
    )

print('pdil_files:\t', p1.pdil_files)

