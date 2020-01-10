import luigi
from src.pipeline.download import Channel

c = Channel(patient_id=1, channel_id=3)

luigi.build([c], local_scheduler=True, workers=5)
