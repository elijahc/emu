import os
import io
import luigi
import pandas as pd
from src.pipeline.io import FileManifest, Patients
from src.pipeline.utils import file_ids_by_channel

root_dir = os.path.expanduser('~/.emu/')

def test_FileManifest():
    tasks = [
        FileManifest(patient_id=1, data_root=root_dir),
    ]
    luigi.build(tasks, local_scheduler=True)
    
    buf = io.StringIO(tasks[0].open('r'))
    files = pd.read_csv(buf)
    print(files)
    return files

def test_BoxPatients():
    tasks = []