#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 18:12:06 2023

@author: elizabethtnguyen
"""

#import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

#def useful functions
def convert_str_to_float(string):
    
    try: 
        x = re.findall(r"[-+]?\d*\.\d+|\d+", string.replace(",",""))[0]
    except:
        x = None
    return x
    
us_state_to_abbrev = {
"Alabama": "AL",
"Alaska": "AK",
"Arizona": "AZ",
"Arkansas": "AR",
"California": "CA",
"Colorado": "CO",
"Connecticut": "CT",
"Delaware": "DE",
"Florida": "FL", 
"Georgia": "GA",
"Hawaii": "HI",
"Idaho": "ID",
"Illinois": "IL",
"Indiana": "IN",
"Iowa": "IA",
"Kansas": "KS",
"Kentucky": "KY",
"Louisiana": "LA",
"Maine": "ME",
"Maryland": "MD",
"Massachusetts": "MA",
"Michigan": "MI",
"Minnesota": "MN",
"Mississippi": "MS",
"Missouri": "MO",
"Montana": "MT",
"Nebraska": "NE",
"Nevada": "NV",
"New Hampshire": "NH",
"New Jersey": "NJ",
"New Mexico": "NM",
"New York": "NY",
"North Carolina": "NC",
"North Dakota": "ND",
"Ohio": "OH",
"Oklahoma": "OK",
"Oregon": "OR",
"Pennsylvania": "PA",
"Rhode Island": "RI",
"South Carolina": "SC",
"South Dakota": "SD",
"Tennessee": "TN",
"Texas": "TX",
"Utah": "UT",
"Vermont": "VT",
"Virginia": "VA",
"Washington": "WA",
"West Virginia": "WV",
"Wisconsin": "WI",
"Wyoming": "WY",
"District of Columbia": "DC"}

#invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

print('start import top us cities')

#define lists
list_city = []
list_state = []
list_state_v2 = []
list_city_state = []


#define options selenium
options = Options()
options.headless = True
    
driver = webdriver.Chrome(options=options, executable_path="/Users/elizabethtnguyen/Desktop/Thomas/chromedriver")
driver.set_window_position(0,0)
driver.set_window_size(0,0)

#loop on state
for state in abbrev_to_us_state.keys():
    
    #redefine state
    state = state.replace(' ','_')
    
    #request access and pull html
    driver.get("https://www.bestplaces.net/find/state.aspx?state={}".format(state.lower()))
    page_source = driver.page_source
    print(state)
    
    for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[5]/div[2]/div[1]/h2"):
        value = element.get_attribute("innerText")
        list_temp = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))
        length_state = int(list_temp[0])
    

    for i in range(0,length_state):
        try:
            for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[5]/div[2]/div[1]/div[3]/div[1]/ul/li[{}]/a/u".format(str(i))):
                list_city.append(element.get_attribute("innerText"))
                list_state.append(state.upper())
        except:
            True
     
        try:
            for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[5]/div[2]/div[1]/div[3]/div[2]/ul/li[{}]/a/u".format(str(i))):
                list_city.append(element.get_attribute("innerText"))
                list_state.append(state.upper())
        except:
            True
       
        try:
            for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[5]/div[2]/div[1]/div[3]/div[3]/ul/li[{}]/a/u".format(str(i))):
                list_city.append(element.get_attribute("innerText"))
                list_state.append(state.upper())
        except:
            True
            
for i in range(0,len(list_state)):
    list_state_v2.append(abbrev_to_us_state[list_state[i]])
    list_city_state.append(list_city[i] + ' ' + abbrev_to_us_state[list_state[i]])
     
data_city = {'City' : list_city, 'State' : list_state_v2, 'City_State' : list_city_state}
data_city = pd.DataFrame(data_city)
data_city.to_excel("List_Cities_States.xlsx")


	

