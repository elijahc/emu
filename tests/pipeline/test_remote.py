from emu.pipeline.remote import RemoteFile
from emu.pipeline.remote import RemoteCSV
from emu.pipeline.remote import RemotePatientManifest

pt_fid = 588757437066

def test_RemoteFile():
    remote_file = RemoteFile(file_id=pt_fid)

def test_RemoteCSV():
    r_csv = RemoteCSV(file_id=pt_fid)

    tab = r_csv.load()
    return tab

def test_RemotePatientManifest():
    return RemotePatientManifest().load()