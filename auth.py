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

    def get_headers(self, market: str = None,
                    amount: str = None,
                    price: str = None,
                    otype: str = None) -> str:

        if self.encryption:
            if self.clientid and self.secretkey:
                body = {}
                try:
                    '''Generating signature'''
                    bSecretKey = bytes(self.secretkey, encoding='utf8')

                    if market and amount and price and otype:
                        body["market"] = market
                        body["amount"] = amount
                        body["price"] = price
                        body["type"] = otype

                    body["timestamp"] = self.timestamp
                    body["validity"] = self.validity

                    sign_body = json.dumps(body, separators=(',', ':'))
                    bBody = bytes(sign_body, encoding='utf8')

                    signature = hmac.new(
                        bSecretKey, bBody, digestmod=hashlib.sha256)

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
                print("Using non-encrypted authorization (NOT RECOMMENDED!)")
                return headers
            else:
                print("Missing parameter; 'apikey'. ")

    def get_signature(self, market: str = None,
                      amount: str = None,
                      price: str = None,
                      otype: str = None) -> str:
        """
        Returning only the signature
        """
        if self.encryption:
            if self.clientid and self.secretkey:
                body = {}
                try:
                    '''Generating signature'''
                    bSecretKey = bytes(self.secretkey, encoding='utf8')

                    if market and amount and price and otype:
                        body["market"] = market
                        body["amount"] = amount
                        body["price"] = price
                        body["type"] = otype

                    body["timestamp"] = self.timestamp
                    body["validity"] = self.validity

                    sign_body = json.dumps(body, separators=(',', ':'))
                    bBody = bytes(sign_body, encoding='utf8')

                    signature = hmac.new(
                        bSecretKey, bBody, digestmod=hashlib.sha256)

                except Exception as e:
                    print(e)

            return signature.hexdigest()

    def get_url_params(self) -> str:
        '''Generating URL-parameters.
        Must be included in URL when using HMAC encrypted secretkey.
        URL-parameter 'timestamp' and 'validity' must match with the
        ones used to generate signature'''

        url = f"?timestamp={self.timestamp}&validity={self.validity}"

        return url
