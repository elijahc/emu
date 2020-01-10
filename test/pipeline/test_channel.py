import luigi
from src.pipeline.process import ChannelTimestamp as Channel

c = Channel(patient_id=1, channel_id=3)

luigi.build([c], local_scheduler=True, workers=5)
