import luigi
import os

from src.pipeline.io import *

task = GetDevelopmentClient()

files = [
    '562127657379',
    '562128317953',
]

task = DownloadRaw(raw_dir=os.path.expanduser('~/dev/emu/raw'), file_ids=files)

outputs = [t.path for t in task.output()]
print(outputs)

