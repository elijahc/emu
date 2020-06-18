import io
from ..pipeline.remote import RemoteCSV

class Participant(object):
    def __init__(self,patient_id, raw_files, results = []):
        self.patient_id = patient_id
        self.all_files = raw_files
        self.results = results
        # self.survey_files = self.all_files.query('type == "CSV"')
        for r in results:
            setattr(self,r.name,r)
            setattr(self,r.name+'_files',r.files())
            setattr(self,'cache_{}'.format(r.name),r.cache)

    def __repr__(self):
        results_list = '\n'.join(['- {}'.format(r.__repr__()) for r in self.results])
        return 'Participant(id={})\n'.format(self.patient_id)+results_list

    def create_nwb(self,nev_fp,ncs_fps,blocks, desc=''):
        if 0 in blocks:
            practice_incl = True
        else:
            practice_incl = False

        if hasattr(self,'electrode_locations'):
            self.nwb = nlx_to_nwb(nev_fp=nev_fp, ncs_paths=ncs_fps,desc=desc,
                                  practice_incl=practice_incl,
                                  electrode_locations=self.electrode_locations)
        else:
            self.nwb = nlx_to_nwb(nev_fp=nev_fp, ncs_paths=ncs_fps,desc=desc,
                                  practice_incl=practice_incl)

        # TODO: implement code below
        # for start,dt,choice in zip(trial_starts,trial_delta,choices.tuple.values):

        #     self.nwb.add_trial(start_time=start,stop_time=start+dt,outcome=choice)