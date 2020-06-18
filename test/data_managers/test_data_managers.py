import os
import pytest
from emu.data_managers import PDILBehavior,Participant,Electrophysiology
from emu.pdil.raw import get_data_manifest

def create_p1():
    data_manifest = get_data_manifest()

    pdil = PDILBehavior(patient_id = 1, raw_files = data_manifest)
    seeg = Electrophysiology(patient_id = 1, raw_files = data_manifest)



    p1 = Participant(patient_id = 1, raw_files=data_manifest, results=[
        pdil,
        seeg,]
        )
    return p1


def test_init():
    p1 = create_p1()

    assert p1.pdil_files != None
    print('pdil_files:\t', p1.pdil_files)
    

if __name__ == "__main__":
    p1 = create_p1()

    print('pdil_files:\t', p1.pdil_files)

