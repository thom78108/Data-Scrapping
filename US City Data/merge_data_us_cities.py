#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 07:05:16 2023

@author: elizabethtnguyen
"""

import pandas as pd
var = True
df_cities_state = pd.read_excel('List_Cities_States.xlsx')

### PART 1 : PULL HIGH LEVEL RESULTS ###

if var == False:
    list_state = []
    list_successes = []
    list_failures = []
    
    
    for state in df_cities_state['State'].unique():
       
       print(state) 
       var_suc = 0
       var_fai = 0
       
       for x in [0,1]:
         
            df_data_successes = pd.read_excel("Successes_{}_{}.xlsx".format(state,x+1))
            df_data_failures = pd.read_excel("Failures_{}_{}.xlsx".format(state,x+1))
            
            var_suc = var_suc + len(df_data_successes)
            var_fai = var_fai + len(df_data_failures)
       
       #add data to list
       list_state.append(state)
       list_successes.append(var_suc)
       list_failures.append(var_fai)
       
       
    data = {"State" : list_state, "Successes" : list_successes, "Failures" : list_failures}
    df = pd.DataFrame(data)    
    df.to_excel("High_Level_Results.xlsx")

### PART 2 : PULL DETAILED RESULTS ###
N = 0

if var == True:
    for state in df_cities_state['State'].unique():
        print(state)
        for x in [0,1]:
           
            df_temp = pd.read_excel("Successes_{}_{}.xlsx".format(state,x+1))
        
            #logic based on index
            if N == 0:
                df_final = df_temp
            else:
                df_final = pd.concat([df_final, df_temp])
            
            N = N + 1
    
    df_final.to_excel("US_Cities_Data.xlsx")
