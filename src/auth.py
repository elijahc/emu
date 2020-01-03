import os
from boxsdk import JWTAuth
from boxsdk import Client, DevelopmentClient

DEFAULT_CONFIG_FP=os.path.expanduser('~/.emu/config.json')

def jwt(cred_fp=DEFAULT_CONFIG_FP):
    # Load JWT config file from default location
    config = JWTAuth.from_settings_file(os.path.expanduser(cred_fp))
    return Client(config)

# class EMU(Client):

#     def get_file_manifest(self, folder_id, out):
#         recs = []
#         for f in self.folder(folder_id):
#             if f.type == 'folder'
#             recs.append({''})

#     def tree(self, folder_id):
#         folder = self.folder(folder_id)
#         folder.get_items()



if __name__ == "__main__":

    auth = Auth()

    client = auth.jwt()

    print(client)
