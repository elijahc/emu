from emu.data_managers import PDILBehavior
from emu.pdil.raw import get_data_manifest


data_manifest = get_data_manifest()

pdil = PDILBehavior(raw_files = all_files)
