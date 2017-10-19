
from __future__ import print_function  # compatibility with python3
import httplib2
import os
from apiclient import discovery  # create  a service endpoint for interacting with an API
from oauth2client import client  # additional resources for authorized data
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-events.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and inserts event into 
    atendee\'s calendars
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    GCAL = discovery.build('calendar', 'v3', http)

    GMT_OFF = '-07:00'      # PDT/MST/GMT-7
    EVENT = {
        'summary': 'Baloonicorns Birthday',
        'start': {'dateTime': '2017-09-05T11:00:00%s' % GMT_OFF},
        'end': {'dateTime': '2017-09-05T12:00:00%s' % GMT_OFF},
        'attendees': [
            {'email': 'eileen.hays@gmail.com'},
            # {'email': ''},
        ],
    }

    e = GCAL.events().insert(calendarId='primary',
                             sendNotifications=True, body=EVENT).execute()

    print('''*** %r event added:
        Start: %s
        End:   %s''' % (e['summary'].encode('utf-8'),
            e['start']['dateTime'], e['end']['dateTime']))

    # service = discovery.build('calendar', 'v3', http=http)
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # eventsResult = service.events().list(
    #     calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
    #     orderBy='startTime').execute()
    # events = eventsResult.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

if __name__ == '__main__':
    main()