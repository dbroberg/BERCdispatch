import smtplib
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from info import me, you, pwd

dayset = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
monthset = ['January','February','March','April','May','June','July',
            'August','September','October','November','December']

class EmailCompiler(object):
    def __init__(self, bercset, nonbercset):
        """
        Compact class for assembling draft email for BERC

        dispatch entries has berc set in [0], non-berc in set [1], (within each there is a pair, first part is for table of contents, second part is details
            note toc entries need to have numbers already written in as well...

        html notes = </p> skips a line and starts a new paragraph
                    </br> is same as \n in python
        """
        self.html = ''
        self.attachment = 'berclogo.png'
        self.imagehtml = '<img src="cid:'+str(self.attachment)+'"><br>'
        self.tocvalues_berc = bercset
        self.tocvalues_nonberc = nonbercset


    def html_creator(self, today='Monday, October 17, 2016'):
        """
        create html script for email

        set today variable to define the date of today
        """

        self.html = """\
        <html>
        <head></head>
        <body>
            <center>
            <p><span style="font-size:8px;font-family:arial;color:rgb(0,0,0);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"><HR WIDTH="60%">
            """+self.imagehtml+"""
            <center><span style="font-size:32px;font-family:diplomata;color:rgb(0,0,0);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">DISPATCH</span></center><br>
            <p><span style="font-size:8px;font-family:arial;color:rgb(0,0,0);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"><HR WIDTH="60%">
            </p>
            <center><span style="font-size:14.6667px;font-family:cambria;color:rgb(0,0,0);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">Berkeley, California - """+str(today)+"""</span></center>
            <p><span style="font-size:8px;font-family:arial;color:rgb(0,0,0);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"><HR WIDTH="60%">
            </center>
            <p><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">Headlines:</span></p>
            <ul style="margin-top:0pt;margin-bottom:0pt"><li dir="ltr" style="list-style-type:disc;font-size:17.3333px;font-family:cambria;color:rgb(0,0,0);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"><p dir="ltr" style="line-height:1.656;margin-top:0pt;margin-bottom:0pt"><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">Highlight 1</span></p></li>
            <li dir="ltr" style="list-style-type:disc;font-size:17.3333px;font-family:cambria;color:rgb(0,0,0);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"><p dir="ltr" style="line-height:1.656;margin-top:0pt;margin-bottom:0pt"><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">Highlight 2</span></p></li>
            <li dir="ltr" style="list-style-type:disc;font-size:17.3333px;font-family:cambria;color:rgb(0,0,0);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"><p dir="ltr" style="line-height:1.656;margin-top:0pt;margin-bottom:0pt"><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">Highlight 3</span></p></li></ul>
            <p dir="ltr" style="line-height:1.656;margin-top:0pt;margin-bottom:0pt"><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"></span></p><hr>
            <span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:italic;font-variant:normal;text-decoration:none;vertical-align:baseline">BERC Events</span>
        """

        #do berc table of contents
        for tind,tocentry in enumerate(self.tocvalues_berc[0]):
            tocentry.replace('\n','<br />')
            self.html+="""<p dir="ltr" style="line-height:1.656;margin-top:0pt;margin-bottom:0pt"><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:italic;font-variant:normal;text-decoration:none;vertical-align:baseline"><a href="#"""+str(tind+1)+"""" target="_self">"""+str(tocentry)+"""</a></span>"""

        #next do non-berc table of contents
        if len(self.tocvalues_nonberc[0]):
            self.html+="""</p><br><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:italic;font-variant:normal;text-decoration:none;vertical-align:baseline">Other Events and Opportunities</span>"""
        for nonberctoc in self.tocvalues_nonberc[0]:
            tind+=1
            self.html+="""<p dir="ltr" style="line-height:1.656;margin-top:0pt;margin-bottom:0pt"><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:italic;font-variant:normal;text-decoration:none;vertical-align:baseline"><a href="#"""+str(tind+1)+"""" target="_self">"""+str(nonberctoc)+"""</span>"""

        #add the sublink to filling dispatch information
        self.html+="""<p dir="ltr" style="line-height:1.656;margin-top:0pt;margin-bottom:0pt">
        <span style="font-size:16px;font-family:cambria;color:rgb(0,0,0);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"></span>
        </p><hr><p dir="ltr" style="line-height:1.656;margin-top:0pt;margin-bottom:0pt"><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">
        Don't see an event that belongs in this newsletter? You can always</span><a href="https://docs.google.com/forms/d/e/1FAIpQLSdQcizmG5hOSzjzQHMhLppHnDgpGUHwbrxA4yID48jW_FMfPw/viewform" style="text-decoration:none" target="_blank">
        <span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"> </span><span style="font-size:17.3333px;font-family:cambria;color:rgb(16,60,192);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;vertical-align:baseline">submit events via this form.</span></a>
        </p><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">
        Looking for a job? Check out</span><a href="http://berc.berkeley.edu/jobs/" style="text-decoration:none" target="_blank">
        <span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"> </span><span style="font-size:17.3333px;font-family:cambria;color:rgb(16,60,192);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;vertical-align:baseline">BERC's Jobs board.</span></a>
        <span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">.</span><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"><br class="m_-8449436374389848411gmail-kix-line-break"></span>"""



        self.html+="""<span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"></span></p><hr><span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">
        <br class="m_-8449436374389848411gmail-kix-line-break"></span>"""

        print '\ntacking onto email...'
        tind = 0
        for toc, fullentry in zip(self.tocvalues_berc[0], self.tocvalues_berc[1]):
            tind+=1
            print toc
            self.html+="""<span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"><a name="""+str(tind)+"""></a>"""+str(toc)+"""</span>
            <span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">
            <br class="m_-8449436374389848411gmail-kix-line-break"></span><pre style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;
            font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">"""+fullentry+"""</pre><hr>"""

        for toc, fullentry in zip(self.tocvalues_nonberc[0], self.tocvalues_nonberc[1]):
            tind +=1
            print toc
            self.html+="""<span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline"><a name="""+str(tind)+"""></a>"""+str(toc)+"""</span>
            <span style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">
            <br class="m_-8449436374389848411gmail-kix-line-break"></span><pre style="font-size:17.3333px;font-family:cambria;color:rgb(26,26,26);background-color:transparent;
            font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline">"""+fullentry+"""</pre><hr>"""

        #use this to end the html script...
        self.html += """
             </p>
          </body>
        </html>
        """
        return

    def send_email(self):
        #after html is created, send the draft email to my gmail account
        print '\nAttempting to send email.'

        msg = MIMEMultipart('alternative')

        todayobj = datetime.datetime.today()
        today = str(todayobj.month)+'/'+str(todayobj.day)+'/'+str(todayobj.year)
        msg['Subject'] = "BERC Dispatch "+today
        msg['From'] = me
        msg['To'] = you

        # Record the MIME types of both parts - text/plain and text/html.
        # part2 = MIMEText(self.html, 'plain')
        part2 = MIMEText(self.html, 'html')
        msg.attach(part2)

        fp = open(self.attachment, 'rb')
        img = MIMEImage(fp.read())
        fp.close()

        img.add_header('Content-ID', '<{}>'.format(self.attachment))
        msg.attach(img)

        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()
        mail.starttls()

        mail.login(me, pwd)
        mail.sendmail(me, you, msg.as_string())
        mail.quit()
        print 'Email sent!'
        return

if __name__ == "__main__":
    s = EmailCompiler([["1) test1, Tuesday", "2) test2, Wednesday"],["I told you this was a test...</p> see...its a test...","yayayayya</br>buttsup"]],[["3) heyo for yayo"],["whatusp man"]])
    s.html_creator()
    # with open('filetest.html','a') as f:
    #     f.write(s.html)
    s.send_email()