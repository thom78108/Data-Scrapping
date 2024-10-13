#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 20:34:17 2023

@author: thomasfrancois
"""

def send_emails():

    import smtplib, ssl
    import pandas as pd 
    import time 
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # read data from local excel input file
    input_data = pd.read_excel('Input Vessel Tracker.xlsx')
    
    # pull data from input file
    for i in range(0,len(input_data)):
        
        
        first_name_customer = input_data['First_name'][i]
        last_name_customer = input_data['Last_name'][i]
        email_customer = input_data['Email'][i]

        if email_customer != 'Metadata':
            message = MIMEMultipart("alternative")
            message["Subject"] = "multipart test"
            message["From"] = 'thomasf76520data@gmail.com'
            message["To"] = email_customer
            
            # Create the plain-text and HTML version of your message
            text = """\
            Hello {},
            
            The data team wants to let you know that your data was successfully scrapped.
            You can find it by clicking on the following link :
            
            Thanks,
            The data team
            """.format(first_name_customer)
            html = """\
            <html>
              <body>
                <p>Hello {},<br>
                   
                <p>The data team wants to let you know that your data was successfully scrapped.<br>
                   You can find it by clicking on the following link : <br>            
                   
                <p>Thanks,<br>
                   The data team <br>
                </p>
              </body>
            </html>
            """.format(first_name_customer)
            
            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            
            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)
            
            # send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login('thomasf76520data@gmail.com', 'mfye lqbm uqsb hmbu')
                server.sendmail('thomasf76520data@gmail.com', email_customer, message.as_string())
            