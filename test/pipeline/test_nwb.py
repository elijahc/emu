import luigi
from pynwb import NWBHDF5IO
from src.pipeline.process import NWB

tasks = [NWB(patient_id=1)]

luigi.build(tasks, local_scheduler=True,workers=4)

io = NWBHDF5IO(tasks[0].output().path, 'r')
nwb = io.read()
print(nwb)
