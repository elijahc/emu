import luigi
from src.pipeline.process import Downsample

tasks = [Downsample(patient_id=1, channel_id=ch+1) for ch in range(10)]

luigi.build(tasks, local_scheduler=True, workers=2)
