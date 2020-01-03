import os
import luigi
import pandas as pd
from ..auth import jwt
from ..utils import get_file_manifest, _get_ch
from ..luigi.box import BoxTarget

def file_ids_by_channel(file_manifest, channel_ids=[16]):
    channels = file_manifest.query('type == "Channel"')
    channels['ch'] = map(_get_ch, channels.filename.values)

    return channels[channels.ch.isin(channel_ids)]

class Channel(luigi.Task):
    patient_id = luigi.Parameter()
    channel_id = luigi.Parameter()
    raw_dir = luigi.Parameter(default=os.path.expanduser('~/.emu/raw'))
    data_dir = luigi.Parameter(default=os.path.expanduser('~/.emu/raw'))

    # def requires(self):
    #     output = {
    #         'patients':Patients(),
    #         'file_manifest',
    #     }
    #     return output
