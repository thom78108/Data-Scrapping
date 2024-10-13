#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 09:55:53 2023

@author: elizabethtnguyen
"""


from multiprocessing import Process



var = True

#import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request
import requests
import pandas as pd
import re
import ssl
from lxml import etree

#def useful functions
def convert_str_to_float(string):
    
    try: 
        x = re.findall(r"[-+]?\d*\.\d+|\d+", string.replace(",",""))[0]
    except:
        x = None
    return x
        
#define N
N = 0 

#list failed cities
list_failures = []

#import top us cities and define functions/variables
if var == True:
    
    print('start import us cities')

    #define lists
    list_population = []
    list_city = []
    list_state = []
    list_city_state = []

    
    #define driver to webscrap data
    
    #define options selenium
    options = Options()
    options.headless = True
    
    #define driver
    driver = webdriver.Chrome(options=options, executable_path="/Users/elizabethtnguyen/Desktop/Thomas/chromedriver")
    #alert = driver.switch_to_alert()
    driver.set_window_position(0,0)
    driver.set_window_size(0,0)

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
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI"}
    
    #invert the dictionary
    abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

    #loop on state
    for state in abbrev_to_us_state.keys():
    #for state in ['Nebraska']:
        
        #request access and pull html
        driver.get("https://www.bestplaces.net/find/state.aspx?state={}".format(state.lower()))
        page_source = driver.page_source
        
        for i in range(0,1000):
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[5]/div[2]/div[1]/div[3]/div[1]/ul/li[{}]/a/u".format(str(i))):
                    temp_city = element.get_attribute("innerText").replace(' ','_')
                    temp_state = abbrev_to_us_state[state.upper()]
                    if "township" not in temp_city:
                        list_city.append(temp_city) 
                        list_state.append(temp_state)
                        list_city_state.append(temp_city + ', ' + temp_state)
            except:
                True
    
    print(len(list_city))
    #export list of city to dataframe
    data_city = {"City" : list_city, "State" : list_state,"City_State":list_city_state}
    df_city = pd.DataFrame(data_city)   
    df_city.to_excel("List_Cities_States.xlsx")
    print('end import us cities')