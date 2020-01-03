import os
import luigi
import io
import pandas as pd
from src.pipeline.download import Channel, Raw
from src.pipeline.utils import file_ids_by_channel
from src.luigi.box import BoxTarget

# ch_files = file_ids_by_channel(files,channel_ids=[8,16])

target = BoxTarget(path='/Doubt/patient_manifest.csv')
target_utf = BoxTarget(path='/Doubt/patient_manifest.csv',format=luigi.format.UTF8)

root_dir = os.path.expanduser('~/.emu/')
tasks = [
    Channel(patient_id=1, channel_id=6),
]

luigi.build(tasks, local_scheduler=True, workers=2, no_lock=False)
