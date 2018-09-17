"""
For google sheets and calendar APIs

Note...I think if this code gets passed on then the next person will need to make sure they have
Google Calendar and Sheets API's configured (google it online and you will see how to do it)

Also note, following might be useful for packages:
pip install --upgrade google-api-python-client
"""
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

from info import berc, nonberc, spreadsheetId


dayset = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
monthset = ['January','February','March','April','May','June','July',
            'August','September','October','November','December']

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class Sheets(object):
    def __init__(self):
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Google Sheets API Python Quickstart'


    def get_credentials(self):
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
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def main(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        rangeNamestart = 'A1:H'
        startrow = 133
        exitloop = False
        while not exitloop:
            startrow+=1
            rangeName = rangeNamestart+str(startrow)
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=rangeName).execute()
            values = result.get('values', [])
            if startrow!=len(values):
                print('retrieved ',startrow,'rows of data')
                exitloop = True

        fields = values.pop(0)
        organized = {}
        datelist = []
        nodates = []

        if not values:
            print('No data found.')
        else:
            for row in values:
                try:
                    dateval = row[2].split('/')
                    date=datetime.date(int(dateval[2]),int(dateval[0]),int(dateval[1]))
                    if date >= datetime.date.today():
                        organized[date] = {}
                        datelist.append(date)
                        for head,val in zip(fields,row):
                            organized[date][head] = val
                except:
                    nodates.append(row)

        datelist.sort()
        print('Found ',len(datelist),' (dated) events coming up...')
        if len(nodates):
            print('WARNING found entries without dates...should go in and correct them:\n')
            for val in nodates:
                print(val,'\n')

        return datelist, organized, nodates


class Calendar(object):
    def __init__(self):
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Google Calendar API Python Quickstart'

    def get_credentials(self):
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
                                       'calendar-python-quickstart.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def main(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        keyset = [u'summary', u'location', u'start',  u'end', u'description']
        #these are other keys for events and may be helpful... = [u'kind', u'status', u'created', u'updated', u'creator',  u'organizer']
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        bercstuff = []
        nonbercstuff = []

        print('\tDo berc events calendar first...')
        for calset, id in berc.items():
            print('\t\tQuerying ',calset)
            eventsResult = service.events().list(
                calendarId=id, timeMin=now, maxResults=200, singleEvents=True,
                orderBy='startTime').execute()
            events = eventsResult.get('items', [])
            if not events:
                print('\t\t\tNo upcoming events found.')
            else:
                print('\t\t\tFound ',len(events),' upcoming events')

            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                tmpdate = (start.split('T'))[0].split('-')
                dateobj = datetime.date(int(tmpdate[0]),int(tmpdate[1]),int(tmpdate[2]))
                toc = event['summary']+', '+dayset[dateobj.weekday()]+', '+str(dateobj.month)+'/'+str(dateobj.day)
                print('\t\t\t\t',toc)

                try:
                    descrip = event['description']
                except:
                    descrip = 'ERROR OCCURED DOWNLOADING DESCRIPTION. COPY AND PASTE FROM CALENDAR ENTRY...' #note that I could paste the link to the page...too lazy to get the key right nwo but it woudl work..

                if ('location' in event.keys()) and ('start' in event.keys()):
                    if 'dateTime' in event['start'].keys():
                        tmptimestart = event['start']['dateTime'].split('T')[1].split('-')[0]
                        tmphrstart = tmptimestart.split(':')[0]
                        minstart = tmptimestart.split(':')[1]
                        tmptimeend = event['end']['dateTime'].split('T')[1].split('-')[0]
                        tmphrend = tmptimeend.split(':')[0]
                        minend = tmptimeend.split(':')[1]
                        if int(tmphrstart)>12:
                            hrstart = int(tmphrstart)-12
                        else:
                            hrstart = tmphrstart
                        if int(tmphrend)>12:
                            hrend = int(tmphrend)-12
                        else:
                            hrend = tmphrend
                        outval = 'Location: '+str(event['location'])+'\nTime: '+str(hrstart)+':'+str(minstart)+'-'+str(hrend)+':'+str(minend)+'\n'+descrip
                    else:
                        outval = 'Location: '+str(event['location'])+'\n'+descrip
                elif 'location' in event.keys():
                    outval = 'Location: '+str(event['location'])+'\n'+descrip
                else:
                    outval = descrip

                bercstuff.append([dateobj,toc,outval])

        print('\tNow do non-berc events...')
        for calset, id in nonberc.items():
            print('\t\tQuerying ',calset)
            eventsResult = service.events().list(
                calendarId=id, timeMin=now, maxResults=200, singleEvents=True,
                orderBy='startTime').execute()
            events = eventsResult.get('items', [])
            if not events:
                print('\t\t\tNo upcoming events found.')
            else:
                print('\t\t\tFound ',len(events),' upcoming events')

            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                tmpdate = (start.split('T'))[0].split('-')
                dateobj = datetime.date(int(tmpdate[0]),int(tmpdate[1]),int(tmpdate[2]))
                toc = event['summary']+', '+dayset[dateobj.weekday()]+', '+str(dateobj.month)+'/'+str(dateobj.day)
                print('\t\t\t\t',toc)

                try:
                    descrip = event['description']
                except:
                    descrip = 'ERROR OCCURED DOWNLOADING DESCRIPTION. COPY AND PASTE FROM CALENDAR ENTRY...' #note that I could paste the link to the page...too lazy to get the key right nwo but it woudl work..

                try:
                    if event['start']:
                        tmptimestart = event['start']['dateTime'].split('T')[1].split('-')[0]
                        tmphrstart = tmptimestart.split(':')[0]
                        minstart = tmptimestart.split(':')[1]
                        tmptimeend = event['end']['dateTime'].split('T')[1].split('-')[0]
                        tmphrend = tmptimeend.split(':')[0]
                        minend = tmptimeend.split(':')[1]
                        if int(tmphrstart)>12:
                            hrstart = int(tmphrstart)-12
                        else:
                            hrstart = tmphrstart
                        if int(tmphrend)>12:
                            hrend = int(tmphrend)-12
                        else:
                            hrend = tmphrend
                        outval = str(event['location'])+', '+str(hrstart)+':'+str(minstart)+'-'+str(hrend)+':'+str(minend)+'\n'+descrip
                    else:
                        outval = str(event['location'])+'\n'+descrip
                except:
                    outval = str(descrip)

                nonbercstuff.append([dateobj,toc,outval])

        return bercstuff, nonbercstuff


if __name__ == '__main__':
    s=Calendar()
    s.main()

