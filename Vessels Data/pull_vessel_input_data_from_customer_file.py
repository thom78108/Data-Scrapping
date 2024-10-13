# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def pull_vessel_input_data_from_customer_file():
    
    # import packages
    import pandas as pd 
    
    # read data from local excel input file
    input_data = pd.read_excel('input_vessel_data_from_customer_file.xlsx')
    
    # return input
    return input_data



