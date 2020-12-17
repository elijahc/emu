import os
import re
import fnmatch
import sys
import pandas as pd
import numpy as np
import hashlib
from tqdm import tqdm as tqdm
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from .luigi.box import ReadableBoxFile,BoxClient, DEFAULT_CONFIG_FP
from .auth import Client

if sys.version_info[0] < 3: 
    # python 2
    from StringIO import StringIO
    from urlparse import urlparse
else:
    # python 3
    from io import StringIO
    from urllib.parse import urlparse

DEFAULT_MANIFEST_FID = 588757437066
RELEVANT_FILES={
    '.ncs':'SEEG',
    '.nev':'SEEG',
    '.nde': 'SEEG',
    'electrode':'SEEG',
    'survey': 'survey',
    'taskoutput.mat': 'Behavior',
    '.asc': 'eyetracking',
    '.edf': 'eyetracking'
}

_parse_ch = lambda fn: re.match('CSC(?P<channel>[0-9]+)(?P<block>_[0-9]{4})?\.ncs',fn)
_get_ch = lambda f: int(_parse_ch(f).group('channel'))
_get_block = lambda f: _parse_ch(f).group('block')

channel_fn_rgx = 'CSC(?P<channel>[0-9]+)(?P<block>_[0-9]{4})?\.ncs'

def create_or_reuse_client(client):
    if client is None:
        return BoxClient()
    else:
        return client

def get_file_type(filename, relevant_files=RELEVANT_FILES):
    for k in relevant_files.keys():
        if 'med_administration' in filename:
            return 'EMR'
        elif k in filename:
            return relevant_files[k]

def load_patients():
    from .pipeline.remote import RemotePatientManifest
    return RemotePatientManifest().load()

def get_file_manifest(folder, prog_bar=False, **kwargs):
    folder = folder.get()

    # if parent is not None:
    #     parent = os.path.join(parent,folder.name)
    # else:
    #     parent = os.path.join('.')

    total_count = folder.item_collection['total_count']
    folder_name = folder.name
    for f in tqdm(folder.get_items(**kwargs),total=total_count,desc=folder_name):
        if isinstance(f,Folder):
            get_file_manifest(f)
        elif isinstance(f, File):
            ftype = get_file_type(f.name)
            rec = {
                'filename':f.name,
                'id':f.id,
                # 'path':os.path.join(parent,f.name),
                'type': ftype,
                'folder': folder_name,
            }
            yield rec

def md5_16(*args):
    h = hashlib.md5()
    for s in args:
        h.update(s.encode())
    return h.hexdigest()[8:24]

def generate_id(firstname,lastname):
    dig = md5_16(firstname.lower(),'-',lastname.lower())
    print('md5:',dig)

    pt_id = ''.join([c for c in dig if c.isdigit()])
    print('patient_id:',pt_id[-4:])

    return pt_id[-4:]

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

    

class Experiment(object):

    def __init__(self, study, patient_id, client=None, pt_manifest_file_id=None):
        self._client = create_or_reuse_client(client)
        if pt_manifest_file_id is None:
            pt_manifest_file_id = DEFAULT_MANIFEST_FID

        self._pt_manifest_file_id = pt_manifest_file_id

        # self.client = client
        self.patient_id = patient_id
        self.study = study

        _pm = load_patients(
            self._client,
            self._pt_manifest_file_id,
            )
        self._patient_manifest = _pm.query('study == "{}"'.format(self.study))
        self._patient_manifest = self._patient_manifest.query('patient_id == {}'.format(self.patient_id))
        self.channels = None

    def __repr__(self):
        if self.patient_id is not None:
            exp_info = ' - Pt {}'.format(self.patient_id)
        else:
            exp_info = ''
        return '<EMU Experiment{}>'.format(exp_info)

    def files(self):
        records = []
        for fold in self._patient_manifest.folder_id:
            root = self._client.folder(fold)
            folder_files = get_file_manifest(root)
            records.extend(folder_files)
        return pd.DataFrame.from_records(records)

    def load_channels(self):
        if self.channels is None:
            channel_files = fnmatch.filter(self.manifest.filename.values, '*.ncs')
            channels = self.manifest[self.manifest.filename.isin(channel_files)]
            channels['ch'] = map(_get_ch,channels.filename.values)
            channels['block'] = map(_get_block,channels.filename.values)
            self.channels = channels

        return self.channels