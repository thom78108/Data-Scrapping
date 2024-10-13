#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Nov 12 11:17:14 2023

@author: thomasfrancois
"""

# import scripts
import pull_vessel_input_data
import scrape_real_time_vessel_output_data_from_website
import scrape_real_time_vessel_output_data_from_customer_file
import send_emails
import time
#import multiprocessing 

# define start time
start = time.time()

# 1 = input data from website, 2 = input data from customer file 
input_type = 1 

# import list of vessels from customer file or website
input_data = pull_vessel_input_data.pull_vessel_input_data(input_type)
N = len(input_data)
print('pull vessel input data done')

# web scrape vessel data based on input file
if input_type == 1 :
    scrape_real_time_vessel_output_data_from_website.scrape_real_time_vessel_output_data_from_website(input_data,input_type,0,N)

if input_type == 2:    
    scrape_real_time_vessel_output_data_from_customer_file.scrape_real_time_vessel_output_data_from_customer_file(input_data,input_type,0,N)
print('scrape real time vessel output data done')

# send email for each customer from input file. No email will be sent if input data come from website
#send_emails.send_emails()
print('send emails done')

end = time.time()
print(end - start)



    