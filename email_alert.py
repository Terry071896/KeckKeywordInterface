import smtplib

# Helper email modules
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import email
import imaplib

class Email_Alert(object):
        def __init__(self, email_send=None, subject='', body=''):
            if email_send is None:
                self._email_send = []
            self._email_send = email_send
            self._subject = subject
            self._body = body
            # sender email address
            self._email_user = 'tfcox2019@gmail.com'

            # sender email passowrd for login purposes
            self._email_password = 'Tf523216'
            self.sent = False
            self.reply = False

        def alert(self, subject=None, body=None):
            if subject is not None:
                self._subject = subject
            if body is not None:
                self._body = body

            while not self.sent or not self.reply:
                if not self.sent:
                    self.sent = self.send()
                else:
                    self.reply = self.receive()

            return True




        def send(self, subject=None, body=None):
            if subject is not None:
                self._subject = subject
            if body is not None:
                self._body = body


            subject = 'EMAIL_SUBJECT'

            msg = MIMEMultipart()
            msg['From'] = self._email_user

            # converting list of recipients into comma separated string
            msg['To'] = ", ".join(self._email_send)

            msg['Subject'] = self._subject

            msg.attach(MIMEText(self._body,'plain'))

            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(self._email_user, self._email_password)
            try:
                server.sendmail(self._email_user,self._email_send,text)
            except smtplib.SMTPRecipientsRefused:
                print('test')
            server.quit()
            return True

        def receive(self):

            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self._email_user, self._email_password)
            mail.list()
            # Out: list of "folders" aka labels in gmail.
            mail.select("inbox") # connect to inbox.
            the_email = str(mail.uid('search', None, '(HEADER Subject "%s")' % (self._subject))[1][0])
            if the_email == 'b\'\'':
                return False
            else:
                return True
