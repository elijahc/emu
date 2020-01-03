import os
import luigi
import io
import pandas as pd
import numpy as np
from src.pipeline.io import FileManifest
from src.pipeline.download import Channel, Raw
from src.pipeline.utils import file_ids_by_channel
from src.luigi.box import BoxTarget

root_dir = os.path.expanduser('~/.emu/')

# Make sure we have the FileManifest for patient 1
pre_tasks = [FileManifest(patient_id=1)]
luigi.build(pre_tasks, local_scheduler=True)

fm_output = pre_tasks[0].output()
with fm_output.open('r') as infile:
    files = pd.read_csv(infile,dtype={'filename':str,'type':str, 'id':np.int,'path':str})

ch_files = file_ids_by_channel(files,channel_ids=[6])
target_dir = os.path.join(root_dir,'raw','pt{}'.format(1))
fetch_channels = []
for fid,fn in zip(ch_files.id.values,ch_files.filename.values):
    fetch_channels.append(Raw(file_id=fid,save_to=target_dir,file_name=fn))

print('Queing up Raw download jobs: ')
for f in fetch_channels:
    print(f)
print()

luigi.build(fetch_channels, local_scheduler=True, workers=5)