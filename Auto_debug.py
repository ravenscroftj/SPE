import os
import smtplib
import time
from email.mime.text import MIMEText
os.system("python SPE.py --debug > debug.txt 2>&1")
fp = open("debug.txt")
server = 'smtp.gmail.com'
recipients = ['YOUREMAIL']
sender = 'workingon...'
message = 'DEBUG'
session = smtplib.SMTP(server)
session.sendmail(sender,recipients,message);
