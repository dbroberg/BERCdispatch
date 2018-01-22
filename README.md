# BERCdispatch
A python code for sending the BERC weekly dispatch. Queries a google calendar and a google form.
If not doing this for BERC Dispatch purposes, then before using, one must create a google API for their email account.
- for google calendar API use this link: https://developers.google.com/google-apps/calendar/quickstart/python
- for google spreadsheets API use this link: https://developers.google.com/sheets/api/quickstart/python 

In addition to the files on this repo, an additional local file named info.py is required (for BERC calendar, can get this file from the previous VP of Membership). 
This file contains the following variables:
- me = 'string of google email to send from'
- you = 'string of google email to send to'
- pwd = 'string of email password'
#berc specific email calendars
- berc = {'BERC Events':  'string url for berc events google calendar',
         'BERC Communities': 'string url for berc communities google calendar'}
- nonberc = {'On-Campus Energy/Resource Events': 'string url for non-berc on campus events google calendar',
         'Off-Campus Energy/Resources Events (BERC)': 'string url for non-berc off campus google calendar'}
#form for dispatch entries
- spreadsheetId = 'string id for google spreadsheet form to use'
