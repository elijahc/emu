import pandas as pd
from emu.auth import jwt
from emu.auth import DEFAULT_CONFIG
from emu.luigi.box import BoxClient
from emu.luigi.box import ReadableBoxFile
from emu.luigi.box import BoxTarget

client = jwt()

test_path = '/2019-07-30_11-04-51/ConfigurationLog/PegasusLastConfiguration.cfg'
pt_manifest = '/EMU/_patient_manifest.csv'
pt_fid = 588757437066

def get_box_client(conf=DEFAULT_CONFIG):
    return BoxClient(path_to_config=conf)

def test_box_client():
    bc = get_box_client()

    box_file = bc.file(pt_fid)
    box_file = box_file.get()

def test_readable_box_file(fid=562610496605):
    bc = get_box_client()
    rbf = ReadableBoxFile(file_id=fid, client=bc)
    return rbf

def test_box_target(test_path=pt_manifest):
    path_target = BoxTarget(path=test_path)
    assert(path_target.exists()==True)

    fid_target = BoxTarget(file_id=pt_fid)