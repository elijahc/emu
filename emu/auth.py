import os
from boxsdk import JWTAuth
from boxsdk import Client

class Auth(object):

    def __init__(self):
        pass

    def jwt(self, cred_fp='~/.emu/credentials.json'):
        # Load JWT config file from default location
        config = JWTAuth.from_settings_file(os.path.expanduser(cred_fp))
        print(config)

        self.config = config

        return Client(config)

if __name__ == "__main__":

    auth = Auth()

    client = auth.jwt()

    print(client)
