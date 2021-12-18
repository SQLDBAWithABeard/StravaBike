import requests
import os
from databaseAccess import setConfig
print('Lets get the tokens')
copied_code = 'a57440ac98008493eebed68c38949c53179d8b5f'
client_id = os.environ.get('CLIENTID')
client_secret = os.environ.get('CLIENTSECRET')

response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': client_id,
                            'client_secret': client_secret,
                            'code': copied_code,
                            'grant_type': 'authorization_code'
                            }
)

strava_tokens = response.json()
if 'message' in strava_tokens:
    print(strava_tokens)
else:
    print('Didnt have message in strava tokens so putting in database')
    setConfig(strava_tokens)