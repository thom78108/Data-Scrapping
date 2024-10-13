#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 16:11:46 2023

@author: thomasfrancois
"""

import pull_vessel_input_data_from_website_file
import pull_vessel_input_data_from_customer_file

def pull_vessel_input_data(input_type):

    if input_type == 1:
        return pull_vessel_input_data_from_website_file.pull_vessel_input_data_from_website_file()
    
    if input_type == 2:
        return pull_vessel_input_data_from_customer_file.pull_vessel_input_data_from_customer_file()   