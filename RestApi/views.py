from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
import uuid
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib, email, os

#https://www.google.com/settings/security/lesssecureapps
@api_view(["POST"])
def sendEmail(request):
    sender_email = "www.aayushrai@gmail.com"
    password = "9893226631"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Coffe Shop Order: Placed"
    message["From"] = sender_email
    part1 = MIMEText("Text which you wnat to send", "plain")
    # part2 = MIMEText(html, "html")
    message.attach(part1)
    # message.attach(part2)
    receivers = ["rai.aayush2000@gmail.com"]
    context = ssl.create_default_context()
    if len(receivers)>0:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                print("Sending emails")
                server.login(sender_email, password)
                for receiver_email in receivers:
                        message["To"] = receiver_email
                        server.sendmail(sender_email, receiver_email, message.as_string())
    else:
        print("No Emails")
    return Response({"email":"ohk"})

#https://stackoverflow.com/questions/33119667/reading-gmail-is-failing-with-imap

@api_view(["GET"])
def getMessages(request):
    user = "www.aayushrai@gmail.com"
    password = "9893226631"
    imap_url = "imap.gmail.com"
    connection = imaplib.IMAP4_SSL(host=imap_url)
    connection.login(user, password)
    connection.select()
    result, data = connection.uid('search', None, "ALL")
    if result == 'OK':
        for num in reversed(data[0].split()):
            result, data = connection.uid('fetch', num, '(RFC822)')
            if result == 'OK':
                email_message = email.message_from_bytes(data[0][1])
                print('From:' + email_message['From'])
                print('To:' + email_message['To'])
                print('Date:' + email_message['Date'])
                print('Subject:' + str(email_message['Subject']))
                print('Content:' + str(email_message.get_payload()[0]))
            
    connection.close()
    connection.logout()
    return Response({"email":"this my email"})