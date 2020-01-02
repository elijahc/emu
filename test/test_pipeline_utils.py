import os
from src.pipeline.utils import *

root_dir = os.path.expanduser('~/.emu/')
tasks = [
    FileManifest(patient_id=1, data_root=root_dir),
]

output = luigi.build(tasks, local_scheduler=True)
