from django.shortcuts import render

# Download the helper library from https://www.twilio.com/docs/python/install
from django.http import HttpResponse
from twilio.rest import Client
import requests


RECOVERY='VTFMQMELDKMR4GVQGF3QLVV9'

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC3c038143d4cabc768aa3720b7e190b88'
auth_token = '69b6e95da441ea43370df5018c8cfca1'
client = Client(account_sid, auth_token)

def send_whatsapp_message(messages, dest) :
    message = client.messages.create(
    from_='whatsapp:+14155238886',  #'+16173373639',
    body=messages,
    to='whatsapp:' + dest  #'whatsapp:+22953297344'
    )

    print('message : ', message.sid)
    return HttpResponse('SMS send successfuly.')

# def send_whatsapp_message(request) :
#     message = client.messages.create(
#     from_='whatsapp:+14155238886',
#     body='Your appointment is coming up on July 21 at 3PM',
#     to='whatsapp:+22961133565'
#     )

#     print(message.sid)
