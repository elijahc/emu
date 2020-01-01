import os
import luigi
from src.pipeline.io import *

files = [
    '562127657379',
    '562128317953',
]

# task = DownloadRaw(raw_dir=os.path.expanduser('~/dev/emu/raw'), file_ids=files)

luigi.build([DownloadRaw(raw_dir=os.path.expanduser('~/dev/emu/raw'), file_id=fid) for fid in files],local_scheduler=True)
# outputs = [t.path for t in task.output()]
# print(outputs)

# class RunAll(luigi.Task):
#     def run(self):
#         pass

# luigi.run(main_task_cls=RunAll, local_scheduler=True)
