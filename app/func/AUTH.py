from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
URL_TO_CRED_FILE='/home/alexovidovich/app/static/credentials.json'
URL_TO_TOKEN_FILE='/home/alexovidovich/app/static/token.json'
def get_creditionals():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(URL_TO_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(URL_TO_TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                URL_TO_CRED_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(URL_TO_CRED_FILE, 'w') as token:
            token.write(creds.to_json())
    
    service = build('calendar', 'v3', credentials=creds)
    print(service)
    return service
