import os
import luigi
import io
import pandas as pd
import numpy as np
import tempfile
from emu.auth import jwt, DEFAULT_ROOT
from emu.pipeline.download import FileManifest
from emu.pipeline.download import Raw, check_or_create, BehaviorRaw
from emu.pipeline.utils import file_ids_by_channel
from emu.luigi.box import BoxTarget

root_dir = DEFAULT_ROOT

files = [
    '562127657379',
    '562128317953',
]

def test_check_or_create():
    temp_dir = tempfile.mkdtemp()
    check_or_create(temp_dir)

    test_path = os.path.join(root_dir, 'path','to','dir')
    check_or_create(test_path)

    assert(os.path.exists(test_path)==True)

def get_file_manifest():
    # Make sure we have the FileManifest for patient 1
    pre_tasks = [FileManifest(patient_id=1)]
    luigi.build(pre_tasks, local_scheduler=True)

    fm_output = pre_tasks[0].output()
    with fm_output.open('r') as infile:
        files = pd.read_csv(infile,dtype={'filename':str,'type':str, 'id':np.int,'path':str}) 

    return files

def test_Raw():
    temp_dir = tempfile.mkdtemp()
    fn = 'test_file.txt'
    lj = Raw(file_id=files[0], save_to=temp_dir, file_name=fn)

    assert(lj.file_id==files[0])
    assert(lj.save_to==temp_dir)
    assert(lj.file_name==fn)
    assert(lj.output().path==os.path.join(temp_dir,fn))

def test_BehaviorRaw():
    assert(False==True)

if __name__ == "__main__":
    # test_check_or_create()

    # test_download_by_channel()
    files = get_file_manifest()

