import pandas as pd
from emu.utils import load_patients

def test_load_patients():
    patients =  load_patients()

    assert(isinstance(patients, pd.core.frame.DataFrame)==True)
    return patients