# Firi API signature generator

Generates complete http headers and URL-parameters for authentication required by the Firi API.

## How to use

1. Import class: Authenticate from module: auth
```python
from auth import Authenticate 
```

2. Declare an instance of the class Authenticate.
```python
instance = Authenticate(argument, argument, ...)
```
3. Pass in required and optional arguments:

### Required arguments: 
For authentication using HMAC-encrypted signature and ClientID (RECOMMENDED):

- secretkey = 'Your Secret Key'
- clientid = 'Your ClientID'

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

auth = Authenticate(userkey=your_secret_key, clientid=you_client_id)

# Return headers:
auth.get_headers() 
# Return URL parameters: 
auth.get_params()
```
### Complete headers with non-encrypted api-key (NOT RECOMMENDED): 
```python
from auth import Authenticate
 
your_api_key = 'Insert API Key'

auth = Authenticate(userkey=your_api_key, encyption=False)

# Return headers:
auth.get_headers() 
```
Returns: 
### Complete headers with client-id + HMAC-encrypted signature, and custom timestamp:
```python
from auth import Authenticate

your_secret_key = 'Insert Secret Key'
your_client_id = 'Insert ClientID'
custom_timestamp = '1671243840'

auth = Authenticate(secretkey=your_secret_key, client_id=your_client_id, timestamp=)

# Return headers: 
auth.get_headers()
# Return URL parameters:
auth.get_url_params()
```