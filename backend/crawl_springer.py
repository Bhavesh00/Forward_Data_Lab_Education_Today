"""
API Resources:
https://dev.springernature.com/
https://dev.springernature.com/example-metadata-response 



API Key (Add this as a user_key parameter to your API calls to authenticate):
e04afc19febd3700b686b4afade1c7db   

"""

import requests

api_key = "e04afc19febd3700b686b4afade1c7db"
response = requests.get("http://api.springernature.com/meta/v2/json?q=doi:10.1007/BF00627098&api_key=" + api_key)
