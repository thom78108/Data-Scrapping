#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 09:27:25 2023

@author: thomasfrancois
"""

# import packages
import pandas as pd 

# read data from local excel input file
input_data = pd.read_excel('input_vessel_data_from_website_file.xlsx')

#define count var
count = 0 

# loop on data 
for i in range(0,len(input_data)): 
    try:
        if input_data['vessel_name'][i][0:4] == 'ONE ' or input_data['vessel_name'][i][0:4] == 'MOL ' or input_data['vessel_name'][i][0:4] == 'NYK ':
            count = count + 1
            print(count)
            print(input_data['vessel_name'][i])
    except:
        True
