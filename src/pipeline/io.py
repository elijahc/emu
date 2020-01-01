import os
import luigi
from boxsdk import DevelopmentClient

class GetDevelopmentClient(luigi.Task):
    def run(self):
        pass

    def output(self):
        return client

class DownloadRaw(luigi.Task):
    file_id = luigi.Parameter()
    raw_dir = luigi.Parameter(default=os.path.expanduser('~/.emu/raw'))
    file_type = luigi.Parameter(default='ncs')

    # def requires(self):
        # return GetDevelopmentClient()

    def run(self):
        client = DevelopmentClient()
        file_name = self.file_id + '.' + self.file_type
        fp = os.path.join(self.raw_dir,file_name)

        with open(fp, 'wb') as open_file:
            client.file(str(self.file_id)).download_to(open_file)
            open_file.close()
            # file_info = client.file(fid).get()
            # print()
            # print(file_info)

    def output(self):
        fp = os.path.join(self.raw_dir,self.file_id + '.' + self.file_type)
        print(fp)
        return luigi.LocalTarget(fp)

if __name__ == "__main__":
    luigi.run()
