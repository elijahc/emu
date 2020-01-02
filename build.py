import os
import luigi
from src.pipeline.io import *

tasks = [DownloadRaw(raw_dir=os.path.expanduser('~/projects/emu/raw'), file_id=fid) for fid in files]

luigi.build(tasks, local_scheduler=True)

# class RunAll(luigi.Task):
#     def run(self):
#         pass

# luigi.run(main_task_cls=RunAll, local_scheduler=True)
