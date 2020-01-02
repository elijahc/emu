from src.pipeline.utils import *

root_dir = '/Users/elijahc/dev/emu/'
tasks = [FileManifest(patient_id=1, data_root=root_dir), Patients(data_root=root_dir)]

output = luigi.build(tasks, local_scheduler=True)