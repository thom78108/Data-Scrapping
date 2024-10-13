#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:12:27 2023

@author: thomasfrancois
"""

def pull_vessel_input_data_from_website_file():

    # import packages
    import pandas as pd 
    from pandasql import sqldf
    
    # read data from local excel input file
    input_data = pd.read_excel('input_vessel_data_from_website_file.xlsx')
    
    # take subset data
    sql_query = ''' 
    SELECT *  
     FROM input_data 
    WHERE TRUE
      --AND(SUBSTR(vessel_name,1,4) = 'ONE ' 
      --AND vessel_imo NOT IN ('No Data','0')  
    ''' 
    
    subset_input_data = sqldf(sql_query)

           
    # return input 
    return subset_input_data