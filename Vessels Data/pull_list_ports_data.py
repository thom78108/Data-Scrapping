#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 12:29:37 2023

@author: thomasfrancois
"""
def pull_list_ports():

    # import packages
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import pandas as pd 
    import json
    import time
    import datetime
    
    
    # check systems
    import sys 
    print(sys.executable)
    
    # define subscription variable
    subscription = True
    
    # set up the driver
    driver = webdriver.Chrome()
    
    # define lists
    List_port_name = []
    List_port_code = []
    List_port_country = []
    List_port_latitude = []
    List_port_longitude = []
    
    # define function to clean lat/lon
    def clean_coordinates(string):
        
        if 'W' in string:
            string = '-' + string
        if 'S' in string:
            string = '-' + string
            
        string = string.replace("'E","").replace("'W","").replace("'N","").replace("'S","").replace("°",".")
        
        return string
    
    # for each page
    for i in range(1,98):
        # enter login link
        driver.get('https://www.gccports.com/ports/latitude-longitude/{}'.format(i))
        time.sleep(5)
        source = driver.page_source
        source_v1 = source.split(' <table cellpadding="5" width="100%" class="table">')[1].split('</table>')[0]
        temp_list = source_v1.split('<tr>')
        print(i)
    
        # add data to lists
        for j in range(2,len(temp_list)):
            List_port_name.append(temp_list[j].split('<td>')[1].split('</td>')[0])
            List_port_code.append(temp_list[j].split('<td>')[2].split('</td>')[0])
            List_port_country.append(temp_list[j].split('<td>')[3].split('</td>')[0])
            List_port_latitude.append(clean_coordinates(temp_list[j].split('<td>')[4].split('</td>')[0]))
            List_port_longitude.append(clean_coordinates(temp_list[j].split('<td>')[5].split('</td>')[0]))
            
    
                       
    # create dataframe
    data = {'port name' : List_port_name, 'port code' : List_port_code, 'port country' : List_port_country, 'port latitude' : List_port_latitude, 'port longitude' : List_port_longitude} 
    df = pd.DataFrame(data)      
    df.to_excel('List_overall_ports.xlsx',index=False)
            
    # quite driver
    driver.quit() 