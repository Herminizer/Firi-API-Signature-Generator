import hashlib
import time
import hmac
import json


class Authenticate:

    def __init__(self, timestamp: str = None, validity='2000', secretkey: str = None, clientid: str = None,  apikey: str = None, body={}, encryption=True):

        self.timestamp = timestamp
        if not timestamp:
            self.timestamp = str(int(time.time()))
        self.validity = validity
        self.secretkey = secretkey
        self.clientid = clientid
        self.apikey = apikey
        self.body = body
        self.encryption = encryption

    def get_headers(self):

        if self.encryption:
            if self.clientid and self.secretkey:
                try:
                    '''Generating signature'''
                    bSecretKey = bytes(self.secretkey, encoding='utf8')
                    signature = hmac.new(bSecretKey, digestmod=hashlib.sha256)

                    self.body['timestamp'] = self.timestamp
                    self.body['validity'] = self.validity

                    sign_body = json.dumps(self.body, separators=(',', ':'))
                    bBody = bytes(sign_body, encoding='utf8')

                    signature.update(bBody)

                except Exception as e:
                    print(e)

                headers = {
                    'Content-Type': 'application/json',
                    'miraiex-user-signature': signature.hexdigest(),
                    'miraiex-user-clientid': self.clientid
                }
                return headers
            else:
                print("Missing parameter; 'secretkey' or 'clientid'.")

        if self.encryption == False:
            if self.apikey:
                headers = {
                    'Content-Type': 'application/json',
                    'miraiex-access-key': self.apikey
                }
                print("Using non-encrypted authorization (NOT RECOMMENDED)")
                return headers
            else:
                print("Missing parameter; 'apikey'. ")

    def get_url_params(self):
        '''Generating URL-parameters. 
        Must be included in URL when using HMAC encrypted secretkey. 
        URL-parameter 'timestamp' and 'validity' must match with the one used to generate signature'''

        url = f"?timestamp={self.timestamp}&validity={self.validity}"

        return url
