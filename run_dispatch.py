"""
A full class for assembling BERC weekly dispatch

Status as of 1/22:
- able to query calendar and forms and assemble them into an email (with option of removing stuff)
- Converts text to html, but doesnt look amazing in final email form (
6/12/17 updates:
- Created symbolic link for input link that is given by user in dispatch input view
- fixed calendar text formatting

Ideas for improvements (in all code sets?):
1) Easy/quick fixes:
- have the code be more discriminatory for dates that are not soon? Probably just want to advertise immediate future stuff? Or possibly
review stage cleanup...



2) More elaborate fixes:
- if got through an email dispatch setup, have an option for restarting from existing files
this would involve dumping and pulling up files. Then maybe could just pull google sheets entries since the files were dumped?
 Would help tremendously with speeding up the process when inserting new things...
 Requires tracking which toc objects were deleted in the first run...

- See if calendar entries could include htmls that are embedded?

- make the middle lines (around logo) adjust to size of the email...

- get text in forms AND calendar to be same format in the html email, specifically line breaks...
(worked on this for a while...it is a harder problem then previously thought.
Probably need to try with a seperate code to get an email with text that has spaces in it...
When this gets figured out....add a line break between location line and description...

Requirements:
Beautiful Soup
Google APIs...
"""

import os
import datetime

from berc_google import Sheets, Calendar
from emailsender import EmailCompiler

dayset = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
monthset = ['January','February','March','April','May','June','July',
            'August','September','October','November','December']

import cgi

def unicodeToHTMLEntities(text):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
    return text


class Dispatch(object):
    def __init__(self):
        pass

    def assemble_dispatch(self, persnickity=False):
        """
        Idea for how to do this:
            1) check excel doc for events that have been posted for beyond this day in future...
            2) query google calendars
            3) Work with user to trim down repeats and inappropriate things...

        set persnickity to True if you want to have an added level of Y/N decisions to be made for dispatch forms being BERC or not BERC affiliated...
        """
        bercset = []
        nonbercset = []
        print('Querying: BERC Newsletter Form (Responses)')
        s=Sheets()
        datekeys, entries, nodates = s.main()
        if persnickity:
            print('----------------\nHelp determine if these events are\n' \
                  ' ("B") Berc events, ("N") Non-berc/Other Events and Opportunities, or ("R") Should be ignored.\n-----------')
            for date in datekeys:
                eventname = str(entries[date]['Name of event'])
                location = str(entries[date]['Location of event'])
                eventtime = str(entries[date]['Time of Event'])
                tocdate = str(date.month)+'/'+str(date.day)
                tocvalue = eventname+', '+dayset[date.weekday()]+', '+str(tocdate)
                if not location and eventtime:
                    outval = eventtime+'\n'
                elif location and not eventtime:
                    outval = location+'\n'
                else:
                    outval = ''
                outval += entries[date]['Description of Event']+'\n'
                outval += entries[date]['Link for information or RSVP']
                print('\n-----------------\n',tocvalue,'\n',outval,'\n-----------------\n'
                       'What does this qualify as? (B=BERC, N=Non-BERC, or R=Remove) ')
                usr_decided = raw_input()
                if usr_decided.upper()=='B':
                    print('\nCool. Adding it to the list of BERC events.\n-------\n')
                    bercset.append([date,tocvalue,outval])
                elif usr_decided.upper()=='N':
                    print('\nCool. Adding it to the list of non-BERC events.\n-------\n')
                    nonbercset.append([date,tocvalue,outval])
                elif usr_decided.upper()=='R':
                    print('\nSkipping this event entry.')
                else:
                    print('\nError occured! Please try again and enter either B,N, or R\n')
                    os.kill()
        else:
            for date in datekeys:
                eventname = str(entries[date]['Name of event'])
                location = str(entries[date]['Location of event'])
                eventtime = entries[date]['Time of Event']
                tocdate = str(date.month)+'/'+str(date.day)
                tocvalue = eventname+', '+dayset[date.weekday()]+', '+str(tocdate)
                if not location and eventtime:
                    outval = eventtime+'\n'
                elif location and not eventtime:
                    outval = location+'\n'
                elif location and eventtime:
                    outval = location+', '+eventtime+'\n'
                else:
                    outval = ''
                outval += entries[date]['Description of Event']+'\n'
                outval += entries[date]['Link for information or RSVP']
                if 'BERC' in tocvalue.upper():
                    print('\nBERC EVENT ADDED-----------------\n',tocvalue,'\n',outval,'\n-----------------\n\n')
                    bercset.append([date,tocvalue,outval])
                else:
                    print('\nNON BERC EVENT ADDED-----------------\n',tocvalue,'\n',outval,'\n-----------------\n\n')
                    nonbercset.append([date,tocvalue,outval])

        print('Querying: Google Calendars')
        c = Calendar()
        tmpberc, tmpnonberc = c.main()
        for entry in tmpberc:
            bercset.append(entry)
        for entry in tmpnonberc:
            nonbercset.append(entry)

        bercset.sort()
        nonbercset.sort()

        satisfied = False
        while not satisfied:
            outputberc = [[],[]]
            outputnonberc = [[],[]]
            print('\n\n-----------------------\nAt this point this is our list of events:\nBERC Events:\n')
            for ind, entry in enumerate(bercset):
                print('(',ind+1,')',entry[1])
                outputberc[0].append('('+str(ind+1)+') '+str(entry[1]))
                outputberc[1].append(unicode(entry[2]).encode('ascii', 'xmlcharrefreplace'))

            if not len(bercset): #this is so code doesn't break when no berc events exist...mainly for debugging
                ind=-1

            print('\nOther Events and Opportunities:')
            for ind1, entry in enumerate(nonbercset):
                print('(',(ind+1)+(ind1+1),')',entry[1])
                outputnonberc[0].append('('+str(ind+1+(ind1+1))+') '+str(entry[1]))
                outputnonberc[1].append(unicode(entry[2]).encode('ascii', 'xmlcharrefreplace'))

            print('\n----\nDo you want to remove any of these? Press return to continue ' \
                  'OR\n1) enter R+number to remove event\n2) enter S to enter showing mode\n'
                  '3) enter M+number to move event to opposite section')
            answer = raw_input()
            if not answer:
                satisfied = True
            elif 'R' in answer.upper():
                answer = answer.upper().lstrip('R')
                try:
                    print('\nRemoving entry ',str(answer))
                    if int(answer) <= len(bercset):
                        delval = int(answer)-1
                        del bercset[delval]
                    else:
                        delval = int(answer)-1-len(bercset)
                        del nonbercset[delval]
                except:
                    print('Problem with your input. Try again, please.')
            elif 'M' in answer.upper():
                answer = answer.upper().lstrip('M')
                try:
                    print('\nMoving entry ',str(answer))
                    if int(answer) <= len(bercset):
                        moveval = int(answer)-1
                        nonbercset.append(bercset[moveval])
                        del bercset[moveval]
                        nonbercset.sort()
                    else:
                        moveval = int(answer)-1-len(bercset)
                        bercset.append(nonbercset[moveval])
                        del nonbercset[moveval]
                        bercset.sort()
                except:
                    print('Problem with your input. Try again, please.')
            elif 'S' in answer.upper():
                print('\nShow and tell mode started. What entry would you like to show? (Press enter to continue)')
                showval = raw_input()
                while showval:
                    try:
                        print('-----\nReview entry ',str(showval),'\n-----\n')
                        if int(showval) <= len(bercset):
                            showint = int(showval)-1
                            print(bercset[showint][1])
                            print(bercset[showint][2],'\n-----------\n')
                        else:
                            showint = int(showval)-1-len(bercset)
                            print(nonbercset[showint][1])
                            print(nonbercset[showint][2],'\n-----------\n')
                    except:
                        print('ERROR occured! Please enter a number in range 1-'+str(len(nonbercset)+len(bercset))+'\n')
                    print('Show another one? (press enter to exit show mode)')
                    showval = raw_input()
            else:
                print('\n------\nInvalid Option! Either do remove mode or show mode!\n----\n')


        #note these need to be [toc, details] with toc list (with numbers already assigned) and details in same order as the toc...
        self.bercset = outputberc
        self.nonbercset = outputnonberc

    def send_draft(self, testing=False, backup=False):
        """
        This sets up and sends the email as shown in the EmailCompiler Class
        Can set testing to True for local testing (without internet connection)
        backup saves a draft of the email to a folder called "backups"
        """
        email = EmailCompiler(self.bercset, self.nonbercset)

        # 'Monday, October 17, 2016' is format of todays date
        todayobj = datetime.datetime.today()
        today = str(dayset[todayobj.weekday()])+', '
        today += str(monthset[int(todayobj.month)-1])+' '
        today += str(todayobj.day)+', '+str(todayobj.year)
        email.html_creator(today = today)
        if testing:
            with open('emailtest.html','w') as f:
                f.write(email.html)
        else:
            email.send_email()

        if backup:
            emailname = 'backup/dispatch_'+str(todayobj.month)+'_'+str(todayobj.day)+'_'+str(todayobj.year)+'.html'
            with open(emailname,'w') as f:
                f.write(email.html)



if __name__ == '__main__':
    s=Dispatch()
    s.assemble_dispatch()
    s.send_draft(testing=False, backup=True)
