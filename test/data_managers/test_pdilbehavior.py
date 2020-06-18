import os
import luigi
from emu.data_managers import PDILBehavior
from emu.pdil.raw import get_data_manifest

data_manifest = get_data_manifest()

pdil = PDILBehavior(patient_id = 1, raw_files = data_manifest)
print('patient_id:\t',pdil.patient_id)
print()

print('raw_path:\t:', pdil.behavior_raw_path)

luigi.build(tasks=list(pdil.cache()),local_scheduler=True)

games = list(pdil.load_game_data())
