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

class GoogleCalendar():
    def __init__(self):
        self.creds = None
        self.service = None
        self.calendar_ids = []
        self.calendar_id = ""
        self.__build()
        self.__get_calendar_ids()

    def __build(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        #Build calendar service
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            print("Successfully built calendar connection!")
        except HttpError as error:
            print('An error occurred: %s' % error)
                
    def create_event(self, summary, description, date):
        event = {
        'summary': summary,
        'description': description,
        'start': {
            'date': date,
            # 'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'date': date,
            # 'timeZone': 'America/Los_Angeles',
        },
        }
        return event

    def insert_event(self, event):
        try: 
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

        except HttpError as error:
            print('An error occurred: %s' % error)
    
    def __get_calendar_ids(self):
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for entry in calendar_list['items']:
                self.calendar_ids.append([entry['summary'].strip(), entry['id']])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    def set_calendar_id(self):
        n = len(self.calendar_ids)
        for i in range(n):
            print(f"({i+1}): {self.calendar_ids[i][0]}")
        
        print(f"Please select a calendar by indicating an index 1 through {n}: ")
        index = int(input()) - 1
        
        if index >= 0 and index < n:
            self.calendar_id = self.calendar_ids[index][1]
            print(f"Calendar successfuly set to {self.calendar_ids[index][0]}!")
        else: 
            print("Invalid calendar!")