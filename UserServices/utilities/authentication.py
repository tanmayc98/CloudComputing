import jwt
from oauth2client.file import Storage
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import oauth2client


SECRET_KEY = "hkBxrbZ9Td4QEwgRewV6gZSVH4q78vBia4GBYuqd09SsiMsIjH"
SCOPE = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
STORAGE = Storage('credentials.storage')


def get_token(json_obj):
    token = jwt.encode(json_obj, SECRET_KEY)
    return token


def authorize_credentials(CLIENT_SECRET):
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials


def refresh_access_token(CLIENT_SECRET):
    client_id = CLIENT_SECRET["installed"]["client_id"]
    client_secret = CLIENT_SECRET["installed"]["client_secret"]
    refresh_token = "my_refresh_token"
    request = Request('https://accounts.google.com/o/oauth2/token',
                      data=urlencode({'grant_type': 'refresh_token',
                                      'client_id': client_id,
                                      'client_secret': client_secret,
                                      'refresh_token': refresh_token}),
                      headers={'Content-Type': 'application/x-www-form-urlencoded',
                               'Accept': 'application/json'}
                      )
    response = json.load(urlopen(request))
    return response['access_token']


def get_credentials(access_token):
    user_agent = "Google Sheets API for Python"
    revoke_uri = "https://accounts.google.com/o/oauth2/revoke"
    credentials = oauth2client.client.AccessTokenCredentials(access_token=access_token, user_agent=user_agent,
                                                             revoke_uri=revoke_uri)
    return credentials
