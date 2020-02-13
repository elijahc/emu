import os
import luigi
import pandas as pd
from ..auth import jwt
from ..utils import get_file_manifest, _get_ch
from ..luigi.box import BoxTarget

def file_ids_by_channel(file_manifest, channel_ids=[16]):
    channels = file_manifest[file_manifest.type=="Channel"].copy()
    channels['ch'] = list(map(_get_ch, channels.filename.values))

    return channels[channels.ch.isin(channel_ids)]
