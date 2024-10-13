#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 16:23:45 2023

@author: elizabethtnguyen
"""


#code 1
import os
import smtplib
import ssl
from email.message import EmailMessage


def send_email(to, subject, message):

    email_address = "thomasf76520@gmail.com"
    email_password = "Newlife12345@@"
    
    context = ssl.create_default_context()

    # create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to
    msg.set_content(message)

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

send_email("elizabethtnguyen1@gmail.com","test","Hello World")


#code 2
import smtplib, ssl
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "thomasf76520@gmail.com"
password = input("Newlife12345@@")

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)
    # TODO: Send email here
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 
    
#code 3
