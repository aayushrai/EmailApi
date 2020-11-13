from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
import uuid
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib, email, os
import re

#https://www.google.com/settings/security/lesssecureapps
@api_view(["POST"])
def sendEmail(request):
    sender_email = "dummy21072000@gmail.com"
    password = "Aayush#21"
    data = request.data
    message = MIMEMultipart("alternative")
    message["Subject"] = data["Subject"]
    message["From"] = sender_email
    part1 = MIMEText(data["Content"], "plain")
    # part2 = MIMEText(html, "html")
    message.attach(part1)
    # message.attach(part2)
    receiver_email = data["To"]
    context = ssl.create_default_context()
    if receiver_email:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                print("Sending emails")
                server.login(sender_email, password)
                message["To"] = receiver_email
                server.sendmail(sender_email, receiver_email, message.as_string())
    else:
        print("No Emails")
    return Response({"email":"ohk"})

#https://stackoverflow.com/questions/33119667/reading-gmail-is-failing-with-imap

@api_view(["GET"])
def getMessages(request):
    user = "dummy21072000@gmail.com"
    password = "Aayush#21"
    imap_url = "imap.gmail.com"
    connection = imaplib.IMAP4_SSL(host=imap_url)
    connection.login(user, password)
    connection.select()
   

    result, data = connection.uid('search', None, "ALL")
    lst = []
    if result == 'OK':
        for num in reversed(data[0].split()):
            result, data = connection.uid('fetch', num, '(RFC822)')
            if result == 'OK':
                email_message = email.message_from_bytes(data[0][1])
                filter_content = re.sub("^[\s\S]*?[\n\r][\n\r]", "", str(email_message.get_payload()[0]))
                dis = {'From' : email_message['From'],'To' : email_message['To'],'Date' : email_message['Date'],'Subject' : str(email_message['Subject']),'Content' : filter_content}
                lst.append(dis)
            
    connection.close()
    connection.logout()
    return Response(lst)