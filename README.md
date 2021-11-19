# Firi API signature generator

Generates complete http headers and URL-parameters for authentication required by the Firi API.

## How to use

1. Import class: Authenticate from module: auth
```python
from auth import Authenticate 
```

2. Declare an instance of the class Authenticate.
```python
instance = Authenticate(argument=str, argument=str, ...)
```
3. Pass in required and optional arguments:

### Required arguments: 
For authentication using HMAC-encrypted signature and ClientID (RECOMMENDED):

- secretkey = 'Your Secret Key'
- clientid = 'Your ClientID'

POST calls require the payload to be included in the HMAC signature body.
All 4 arguments must be included, else the method will return body with only timestamp and validity.
```python
auth.get_headers(market="ETHNOK",
                 amount="0.001",
                 price="38000",
                 otype="ask") 
```

For authentication using non-encrypted API Key. To avoid unintended use of API Key, var encryption must be set to 'False'. (NOT RECOMMENDED):

- apikey = 'Your API Key'
- encryption = False

### Optional arguments:
Optional arguments are customizable parameters, but are not required.

#### argument : type 
- timestamp : str
- validity : str
- encryption : True or False


## Example Usage

### Complete headers with client-id, HMAC-encrypted user-signature and required URL-parameters:
```python
from auth import Authenticate
 
your_secret_key = 'Insert Secret Key'
your_client_id = 'Insert ClientID'

auth = Authenticate(secretkey=your_secret_key, clientid=your_client_id)

# Return headers:
auth.get_headers() 
# Return URL parameters: 
auth.get_url_params()
```
### Complete headers for POST calls, including payload in HMAC signature body:
```python
from auth import Authenticate
 
your_secret_key = 'Insert Secret Key'
your_client_id = 'Insert ClientID'

auth = Authenticate(secretkey=your_secret_key, clientid=your_client_id)

# Return headers:
auth.get_headers(market="ETHNOK",
                 amount="0.001",
                 price="38000",
                 otype="ask") 
# Return URL parameters: 
auth.get_url_params()
```
### Only HMAC encrypted signature, with custom parameters 'timestamp' and 'validity' (both optional): 
```python
from auth import Authenticate

your_secret_key = 'RTk2eNs67Vpan3345pmrwYEBYsWXRXtGF3BKTFq8WMLLOLOL'

time_in_epoch = '1671243840'
sign_valid_time = '2000'

auth = Authenticate(secretkey=your_secret_key,
                    timestamp=time_in_epoch, validity=sign_valid_time)

signature = auth.get_signature()

print(signature)
```
### Complete headers with non-encrypted api-key (NOT RECOMMENDED): 
```python
from auth import Authenticate
 
your_api_key = 'Insert API Key'

auth = Authenticate(userkey=your_api_key, encryption=False)

# Return headers:
auth.get_headers() 
```
### Complete headers with client-id + HMAC-encrypted signature, and custom timestamp:
```python
from auth import Authenticate

your_secret_key = 'Insert Secret Key'
your_client_id = 'Insert ClientID'
custom_timestamp = '1671243840'

auth = Authenticate(secretkey=your_secret_key, client_id=your_client_id, timestamp=custom_timestamp)

# Return headers: 
auth.get_headers()
# Return URL parameters:
auth.get_url_params()
```

### Full example of POST request using HMAC encrypted signature:
```python
from auth import Authenticate
import requests

auth = Authenticate(secretkey='Your SecretKey',
                    clientid='Your ClientId',)

# Payload must match with signature body, byte by byte
payload = {
    "market": "ETHNOK",
    "amount": "0.001",
    "price": "30000",
    "type": "bid"
}

# To be included in url
url_parameters = auth.get_url_params()

# Full POST request header (with payload)
headers_POST = auth.get_headers(market=payload["market"],
                               amount=payload["amount"],
                               price=payload["price"],
                               otype=payload["type"])

url = 'https://api.miraiex.com/v2/orders' + url_parameters

requests.post(url, json=payload, headers=headers_POST)

"""
Response [201]:
{'id': 2001333829}
"""
```