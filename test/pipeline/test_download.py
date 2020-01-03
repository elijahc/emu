import os
import luigi
import pandas as pd
from src.pipeline.download import Channel, Raw
from src.pipeline.utils import file_ids_by_channel

# ch_files = file_ids_by_channel(files,channel_ids=[8,16])

root_dir = os.path.expanduser('~/.emu/')
tasks = [
    Channel(patient_id=1, channel_id=6),
]

luigi.build(tasks, local_scheduler=True)