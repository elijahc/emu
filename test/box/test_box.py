import pandas as pd
from src.auth import jwt,DEFAULT_CONFIG_FP
from src.luigi.box import *

client = jwt()

test_path = '/2019-07-30_11-04-51/ConfigurationLog/PegasusLastConfiguration.cfg'
pt_manifest = '/Doubt/patient_manifest.csv'
pt_fid = 588757437066

bc = BoxClient(path_to_config=DEFAULT_CONFIG_FP)

def test_readable_box_file(fid=562610496605):
    rdf = ReadableBoxFile(file_id=fid, client=bc)
    return rdf

def test_box_target(test_path=test_path):
    target = BoxTarget(DEFAULT_CONFIG_FP,pt_manifest)
    with target.open('r') as infile:
        print(infile)
# fid = path_to_fid(client, '/ConfigurationLog')

rbf = ReadableBoxFile(file_id=pt_fid, client=bc)

print('Assigning BoxTarget')
target = BoxTarget(DEFAULT_CONFIG_FP,pt_manifest)

with target.open('r') as infile:
    content = infile.read()
    pts = pd.read_csv(io.StringIO(content))