import os
import luigi
from ..pipeline.process import PDilTask
from ..pipeline.download import Raw, check_or_create
from ..utils import Experiment

def download_experiment(patient_id, data_root='~/.emu/',local_scheduler=True):
    data_root = os.path.expanduser(data_root)
    exp = Experiment(study='pdil', patient_id=patient_id)
    exp_files = exp.files()
    print('filtering for files ending with taskoutput.mat')
    task_output_files = exp_files[exp_files.filename.isin(filter(lambda s: s.endswith('taskoutput.mat'),exp_files.filename))]
    print('downloading...')
    tasks = []
    for i,row in task_output_files.iterrows():
        tasks.append(PDilRaw(patient_id=patient_id,file_id=row.id,file_name=row.filename))
    
    luigi.build(tasks,local_scheduler=local_scheduler)

    return [t.output().path for t in tasks]

class PDilRaw(Raw):
    data_root = luigi.Parameter(default=os.path.expanduser('~/.emu/'))
    study = luigi.Parameter(default='pdil')
    patient_id = luigi.IntParameter()
    save_to = luigi.Parameter(default=None)

    def save_to_dir(self):
            if self.save_to is None:
                return os.path.join(
                    self.data_root,
                    self.study,
                    'pt_{:02d}'.format(self.patient_id),
                    'Behavior'
                    )
            else:
                return self.save_to