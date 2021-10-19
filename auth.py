import hashlib
import time
import hmac
import json


class Authenticate:

    def __init__(self, timestamp: str = None, validity: str = '2000',
                 secretkey: str = None, clientid: str = None,
                 apikey: str = None, encryption: bool = True):

        self.timestamp = timestamp
        if not timestamp:
            self.timestamp = str(int(time.time()))
        self.validity = validity
        self.secretkey = secretkey
        self.clientid = clientid
        self.apikey = apikey
        self.encryption = encryption

    def get_headers(self) -> str:

        if self.encryption:
            if self.clientid and self.secretkey:
                body = {}
                try:
                    '''Generating signature'''
                    bSecretKey = bytes(self.secretkey, encoding='utf8')
                    signature = hmac.new(bSecretKey, digestmod=hashlib.sha256)

                    body['timestamp'] = self.timestamp
                    body['validity'] = self.validity

                    sign_body = json.dumps(body, separators=(',', ':'))
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

        if not self.encryption:
            if self.apikey:
                headers = {
                    'Content-Type': 'application/json',
                    'miraiex-access-key': self.apikey
                }
                print("Using non-encrypted authorization (NOT RECOMMENDED)")
                return headers
            else:
                print("Missing parameter; 'apikey'. ")

    def get_signature(self) -> str:
        body = {}
        try:
            '''Generating signature'''
            bSecretKey = bytes(self.secretkey, encoding='utf8')
            signature = hmac.new(bSecretKey, digestmod=hashlib.sha256)
            body['timestamp'] = self.timestamp
            body['validity'] = self.validity
            sign_body = json.dumps(body, separators=(',', ':'))
            bBody = bytes(sign_body, encoding='utf8')
            signature.update(bBody)
            return signature.hexdigest()
        except Exception as e:
            return e

    def get_url_params(self) -> str:
        '''Generating URL-parameters.
        Must be included in URL when using HMAC encrypted secretkey.
        URL-parameter 'timestamp' and 'validity' must match with the
        one used to generate signature'''

        url = f"?timestamp={self.timestamp}&validity={self.validity}"

        return url
