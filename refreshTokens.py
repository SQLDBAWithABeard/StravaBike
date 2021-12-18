import requests
import time
import databaseAccess
import os
print('Starting refresh Tokens')
client_id = os.environ.get('CLIENTID')
client_secret = os.environ.get('CLIENTSECRET')
strava_tokens = databaseAccess.getConfig() 
expires_at = strava_tokens['expires_at']
print(f'Found expires at {expires_at}')
if strava_tokens['expires_at'] < time.time():
    print('Need a new token from Refresh Tokens')   
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': client_id,
                                'client_secret': client_secret,
                                'grant_type': 'refresh_token',
                                'refresh_token': strava_tokens['refresh_token']
                                }
                    )
    new_strava_tokens = response.json()
    databaseAccess.setConfig(new_strava_tokens)
    # Use new Strava tokens from now
    strava_tokens = new_strava_tokens
else:
    print('token is good')   
print('Finished refresh Tokens Refresh Tokens')