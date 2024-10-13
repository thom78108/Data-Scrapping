#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:12:27 2023

@author: thomasfrancois
"""

def scrape_vessel_input_data_from_website(j):
    
    # import packages
    import selenium
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import pandas as pd 
    import json
    import time
    import datetime
    
    # check systems
    import sys 
    print(sys.executable)
    
    # set up the driver
    driver = webdriver.Chrome()
    
    # enter login link
    driver.get('https://www.vesselfinder.com/login')
    a = driver.find_element(By.NAME, "email")
    b = driver.find_element(By.NAME, "password")
    c = driver.find_element(By.ID, "loginbtn")
    time.sleep(2)
    a.send_keys("thomasf76520@gmail.com")
    b.send_keys("kV51G1We")
    time.sleep(2)
    c.click()
    
    time.sleep(2)
    
    # execute random javascript
    #js = 'alert("Hello World")'
    #river.execute_script(js)
    
    # create lists
    List_vessel_name = []
    List_vessel_imo = [] 
    List_vessel_type = [] 
    List_vessel_eta = []   
    List_vessel_destination_city_port = []   
    List_vessel_destination_country_port = [] 
    List_vessel_speed_knot = [] 
    List_vessel_year_built = []  
    List_vessel_gt = [] 
    List_vessel_dwt = [] 
    List_vessel_sizes_meters = []  
    
    for i in range(1,704):
        
        print('page {}'.format(i))
        
        # enter vessel finder link 
        #type 1 is unknown, 2 is high speed vessels, 3 is passenger/cruise ships, #4 is cargo vessels, #5 is fishing ships, #6 is tankers, #7 military vessels and #8 is yatchs/sailing vessels
        driver.get('https://www.vesselfinder.com/pro/map#vessels?page={}&name=&type={}&flag=-&minYear=0&maxYear=0&minLength=0&maxLength=0&minGT=0&maxGT=0&minDW=0&maxDW=0&sort=0&sortDir=3'.format(i,j))
        
        # pause 5 seconds
        time.sleep(5)
        
        # increase lenght of page by increasing to 100 rows
        select = Select(driver.find_element(By.XPATH, '//*[@id="ui-listing-0"]/div[4]/div[2]/select'))
        time.sleep(1)
        select.select_by_visible_text("100")
                
        # pull page source
        source = driver.page_source
        source_v1 = source.split('ship-photo')
        
        # pull vessel high level data
        for j in range(1,len(source_v1)):
            try: 
                vessel_name = source_v1[j].split('alt="')[1].split('"><!')[0]
            except: 
                vessel_name = 'No data'
                #print('failure vessel')
            try: 
                vessel_imo = source_v1[j].split('imo=')[1].split('&amp;')[0]
            except: 
                vessel_imo = 'No data'
                #print('failure imo')
            try: 
                vessel_eta = source_v1[j].split('<div class="col-eta2 eta2-v1 col-inner">')[1].split('<!---')[0]
            except: 
                vessel_eta = 'No data'
                #print('failure eta')
            try: 
                vessel_destination_city_port = source_v1[j].split('></span>')[1].split('<!---')[0]
            except: 
                vessel_destination_city_port = 'No data'
                #print('failure city port')
            try: 
                vessel_destination_country_port = source_v1[j].split('title="')[1].split('" style="')[0]
            except: 
                vessel_destination_country_port = 'No data'
                #print('failure country port')
            try: 
                vessel_speed_knot = source_v1[j].split('<div class="status-c2">')[1].split('<!---')[0]
            except: 
                vessel_speed_knot = 'No data'
                #print('failure knot')
            try: 
                vessel_type = source_v1[j].split('</div><div class="_3lvwZ">')[1].split('<!---')[0]
            except: 
                vessel_type = 'No data'
                #print('failure knot')
            try: 
                vessel_year_built = source_v1[j].split('<div class="col-year year-v1 col-inner">')[1].split('<!---')[0]
            except: 
                vessel_year_built = 'No data'
                #print('year_built')  
            try: 
                vessel_gt = source_v1[j].split('<div class="col-gt gt-v1 col-inner">')[1].split('<!---')[0]
            except: 
                vessel_gt = 'No data'
                #print('year_built')  
            try: 
                vessel_dwt = source_v1[j].split('<div class="col-dwt dwt-v1 col-inner">')[1].split('<!---')[0]
            except: 
                vessel_dwt = 'No data'
                #print('year_built')  
            try: 
                vessel_sizes_meters = source_v1[j].split('<div class="col-sizes sizes-v1 col-inner">')[1].split('<!---')[0]
            except: 
                vessel_sizes_meters = 'No data'
                #print('year_built')  
                     
            #print(speed_knot)
            #print(vessel_name + ' - ' + vessel_imo)
            
            # clean data 
            if len(vessel_name)>30:
                vessel_name = 'No data'
            if len(vessel_imo)>30:
                vessel_imo = 'No data'
            if len(vessel_type)>30:
                vessel_type = 'No data'
            if len(vessel_name)>30:
                vessel_name = 'No data'
            if len(vessel_eta)>30:
                vessel_eta = 'No data'
            if len(vessel_destination_city_port)>30:
                vessel_destination_city_port = 'No data'
            if len(vessel_destination_country_port)>30:
                vessel_destination_country_port = 'No data'
            if len(vessel_speed_knot)>10:
                vessel_speed_knot = 'No data'
            if len(vessel_year_built)>10:
                vessel_year_built = 'No data'
            if len(vessel_gt)>10:
                vessel_gt = 'No data'
            if len(vessel_dwt)>10:
                vessel_dwt = 'No data'
            if len(vessel_sizes_meters)>10:
                vessel_sizes_meters = 'No data'
               
            
            # add to lists after cleaning data
            List_vessel_name.append(vessel_name)
            List_vessel_imo.append(vessel_imo)
            List_vessel_type.append(vessel_type)
            List_vessel_eta.append(vessel_eta)  
            List_vessel_destination_city_port.append(vessel_destination_city_port)
            List_vessel_destination_country_port.append(vessel_destination_country_port)
            List_vessel_speed_knot.append(vessel_speed_knot)
            List_vessel_year_built.append(vessel_year_built)  
            List_vessel_gt.append(vessel_gt)
            List_vessel_dwt.append(vessel_dwt)  
            List_vessel_sizes_meters.append(vessel_sizes_meters)  
        
            
    # create dataframe
    data = {'vessel_name' : List_vessel_name, 'vessel_imo' : List_vessel_imo, 'vessel_type' : List_vessel_type, 'vessel_eta' : List_vessel_eta, 'vessel_destination_city_port' : List_vessel_destination_city_port, 'vessel_destination_country_port' : List_vessel_destination_country_port, 'vessel_speed_knot' : List_vessel_speed_knot, 'vessel_year_built' : List_vessel_year_built, 'vessel_gt' : List_vessel_gt, 'vessel_dwt' : List_vessel_dwt, 'vessel_sizes_meters' : List_vessel_sizes_meters}
            
    df = pd.DataFrame(data)      
    df.to_excel('input_vessel_data_from_website_file_{}.xlsx'.format(j),index=False)
    
    #write text file
    with open('readme.txt', 'w') as f:
        f.write(source)
        
        
            
scrape_vessel_input_data_from_website(3)      
        
            