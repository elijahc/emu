import luigi
import os
import io
import numpy as np
import pandas as pd
from ..auth import jwt, DEFAULT_ROOT
from .utils import file_ids_by_channel
from ..utils import get_file_manifest,DEFAULT_MANIFEST_FID
from ..luigi.box import BoxTarget

class RemoteCSV(luigi.ExternalTask):
    file_id = luigi.IntParameter(default=None)
    file_path = luigi.Parameter(default=None)

    def output(self):
        if self.file_id is None and self.file_path is None:
            raise ValueError('file_id or file_path must be provided')
        else:
            return BoxTarget(path=self.path,file_id=self.file_id)

class RemotePatientManifest(RemoteCSV):
    # file_id = luigi.IntParameter(default=DEFAULT_MANIFEST_FID)
    patient_id = luigi.IntParameter()

    def output(self):
        return BoxTarget('/EMU/_patient_manifest.csv')

# For backwards compatibility
Patients = RemotePatientManifest