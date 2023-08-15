import hvac
import credentials

class Vault():
    def __init__(self):
        self.response = None
        self.creds = credentials.Credentials()
        self.client = self.client()

    def client(self):
        client = hvac.Client(
            url=self.creds.get_hvac_addr(),
            token=self.creds.get_hvac_token(),
        )
        return client

    def get_response(self):
        path = self.creds.get_hvac_path()
        self.response = self.client.secrets.kv.read_secret_version(path=path)

        return self.response['data']['data']
