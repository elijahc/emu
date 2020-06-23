import os
import pandas as pd
import glob

from emu.pdil.raw import Electrophysiology, Participant
# from emu.pipeline.remote import RemoteStudyManifest
from emu.pipeline.download import ExperimentManifest

# p1_files = RemoteStudyManifest(study='pdil').create()
exp_manifest = ExperimentManifest(study='pdil')
if not exp_manifest.output().exists():
    exp_manifest.run()
p1_files = pd.read_csv(exp_manifest.output().path)

p1 = Participant(patient_id=6305,raw_files=p1_files,seeg_raw_path=os.path.expanduser('~/.emu/pdil/pt_6305/SEEG/raw'))

seeg = Electrophysiology(patient_id=6305, box_files=p1_files, raw_path=os.path.expanduser('~/.emu/pdil/pt_6305/SEEG/raw'))

ncs_files = glob.glob(os.path.expanduser('~/.emu/pdil/pt_01/SEEG/raw/*.ncs'))
nev_file = glob.glob(os.path.expanduser('~/.emu/pdil/pt_01/SEEG/raw/*.nev'))[0]
