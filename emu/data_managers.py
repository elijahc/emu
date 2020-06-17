from .pipeline.download import BehaviorRaw

class PDILBehavior(object):
    def __init__(self,raw_files):
        self.behavior_files = raw_files.query('type == "Behavior"')
    
    def cache(self,verbose=False):
        """
        Yields
        ------
        luigi.Task
            Yields a BehaviorRaw task for downloading a single behavior file
        """
        for i,row in self.behavior_files.iterrows():
            t = BehaviorRaw(
                patient_id=row.patient_id,
                file_id=row.id,
                file_name=row.filename,
                save_to=self.behavior_raw_path,
            )
            yield t

class Participant(object):
    def __init__(self,patient_id, raw_files, results = []):
        self.patient_id = patient_id
        self.all_files = raw_files
        self.survey_files = self.all_files.query('type == "CSV"')
        self.seeg_files = self.all_files.query('type == "SEEG"')
        if 'electrode_locations.csv' in self.all_files.filename.values:
            loc = self.all_files[self.all_files.filename.isin(['electrode_locations.csv'])].iloc[0]
            self.electrode_locations = RemoteCSV(file_id=loc.id).load()