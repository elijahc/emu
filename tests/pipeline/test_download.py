import os
import luigi
import io
import pandas as pd
import numpy as np
from src.auth import jwt, DEFAULT_ROOT
from src.pipeline.io import FileManifest
from src.pipeline.download import Channel, Raw, check_or_create
from src.pipeline.utils import file_ids_by_channel
from src.luigi.box import BoxTarget

root_dir = DEFAULT_ROOT

def test_check_or_create():
    test_path = os.path.join(root_dir, 'path','to','dir')

    check_or_create(test_path)

def test_download_by_channel():
    # Make sure we have the FileManifest for patient 1
    pre_tasks = [FileManifest(patient_id=1)]
    luigi.build(pre_tasks, local_scheduler=True)

    fm_output = pre_tasks[0].output()
    with fm_output.open('r') as infile:
        files = pd.read_csv(infile,dtype={'filename':str,'type':str, 'id':np.int,'path':str})

    ch_files = file_ids_by_channel(files,channel_ids=[6])
    target_dir = os.path.join(DEFAULT_ROOT,'pt{}'.format(1),'sEEG','raw')
    fetch_channels = []
    for fid,fn in zip(ch_files.id.values,ch_files.filename.values):
        fetch_channels.append(Raw(file_id=fid,save_to=target_dir,file_name=fn))

    print('Queing up Raw download jobs: ')
    for f in fetch_channels:
        print(f)
    print()

    luigi.build(fetch_channels, local_scheduler=True, workers=5)

def get_file_manifest():
    # Make sure we have the FileManifest for patient 1
    pre_tasks = [FileManifest(patient_id=1)]
    luigi.build(pre_tasks, local_scheduler=True)

    fm_output = pre_tasks[0].output()
    with fm_output.open('r') as infile:
        files = pd.read_csv(infile,dtype={'filename':str,'type':str, 'id':np.int,'path':str}) 

    return files

def test_download_first_interval():
    files = get_file_manifest()

    # interval_files = file_ids_by_channel(files,channel_ids=[6])
    # target_dir = os.path.join(DEFAULT_ROOT,'pt{}'.format(1),'sEEG','raw') 

    # fetch_channels = []
    # for fid,fn in zip(ch_files.id.values,ch_files.filename.values):
    #     fetch_channels.append(Raw(file_id=fid,save_to=target_dir,file_name=fn))


if __name__ == "__main__":
    # test_check_or_create()

    # test_download_by_channel()
    files = get_file_manifest()

