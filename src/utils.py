import os
import re
import fnmatch
import pandas as pd
import io
from tqdm import tqdm as tqdm
from boxsdk.object.file import File
from boxsdk.object.folder import Folder

_parse_ch = lambda fn: re.match('CSC(?P<channel>[0-9]+)(?P<block>_[0-9]{4})?\.ncs',fn)
_get_ch = lambda f: _parse_ch(f).group('channel')
_get_block = lambda f: _parse_ch(f).group('block')

def load_patients(client, file_id):
    pt_manifest = client.file(file_id).get()
    f = io.StringIO()
    f.write(str(pt_manifest.content()))
    f.seek(0)
    return pd.read_csv(f)

def get_file_manifest(folder, parent=None, prog_bar=False, **kwargs):
    if parent is not None:
        parent = os.path.join(parent,folder.name)
    else:
        parent = os.path.join('.')

    folder_info = folder.get()
    total_count = folder_info.item_collection['total_count']
    for f in tqdm(folder.get_items(**kwargs),total=total_count):
        if isinstance(f,Folder):
            get_file_manifest(f, parent=parent)
        elif isinstance(f, File):
            rec = {
                'filename':f.name,
                'id':f.id,
                'path':os.path.join(parent,f.name),
            }
            yield rec

class Experiment(object):
    _pt_manifest_file_id = 588757437066

    def __init__(self, client, pt_manifest):
        self._client = client
        self.client = client
        self._patient_manifest = load_patients(client, self._pt_manifest_file_id)
        self.patient_id = None
        self.channels = None

    def __repr__(self):
        if self.patient_id is not None:
            exp_info = ' - Pt {}'.format(self.patient_id)
        else:
            exp_info = ''
        return '<EMU Experiment{}>'.format(exp_info)

    def files(self, patient_id):
        self.patient_id = patient_id
        self.folder_id = self._patient_manifest.query('patient_id == {}'.format(patient_id)).iloc[0].folder_id
        root = self.client.folder(self.folder_id)
        self.folder_info = root.get()

        records = get_file_manifest(root)
        self.manifest = pd.DataFrame.from_records(records)

    def load_channels(self):
        if self.channels is None:
            channel_files = fnmatch.filter(self.manifest.filename.values, '*.ncs')
            channels = self.manifest[self.manifest.filename.isin(channel_files)]
            channels['ch'] = map(_get_ch,channels.filename.values)
            channels['block'] = map(_get_block,channels.filename.values)
            self.channels = channels

        return self.channels
