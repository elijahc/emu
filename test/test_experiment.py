from src.auth import jwt
from src.utils import *

PATIENTS_FID = 588757437066

client = jwt()
patients = load_patients(client, PATIENTS_FID)

exp_folder_id = patients.folder_id.values[0]

exp = Experiment(client, patients)
