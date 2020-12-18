import pandas as pd
from emu.utils import load_patients
from emu.utils import md5_16
from emu.utils import generate_id

def test_load_patients():
    patients =  load_patients()

    assert(isinstance(patients, pd.core.frame.DataFrame)==True)
    return patients

def test_md5_16():
    return md5_16('elijah','-','christensen')

def generate_id():
    return generate_id(firstname='elijah',lastname='christensen')
