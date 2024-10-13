#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 22:18:45 2023

@author: thomasfrancois
"""

def scrape_real_time_vessel_output_data_from_website(input_data,input_type,start_input,end_input):
    
    # import packages
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
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
    
    # read static list port data and transform to dictionary
    port_data = pd.read_excel('List Overall Ports.xlsx')   
    port_data_dic = {}
    for i in range(0,len(port_data)):
        port_data_dic[port_data['port name'][i]] = []
        port_data_dic[port_data['port name'][i]].append([port_data['port latitude'][i],port_data['port longitude'][i]])

    
    # read import data file 
    input_data = input_data
    
    # define chrome options and set up the driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2,})
    #options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    
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
        
    # pull data from input file
    for i in range(start_input,end_input):
        
        # input from website
        if input_type == 1:
            
            vessel_name = input_data['vessel_name'][i]
            first_name = 'Main'
            last_name = 'Metadata'
            email = 'Metadata'
            vessel_imo = input_data['vessel_imo'][i]
 
        
        # input from customer file
        elif input_type == 2:
            
            first_name = input_data['first_name'][i]
            last_name = input_data['last_name'][i]
            email = input_data['email'][i]
            # note : we assume each entry has only one vessel to scrape. In future add a loop here to account for entries with multiple vessels
            vessel_imo = list(input_data['list_vessels'])[i].replace('[','').replace(']','')
        
        # default current utc time
        current_time_utc = str(datetime.datetime.now())
        
        # print first name + imo 
        print(first_name + ' ' + vessel_imo + ' ' + str(i))

        # enter vessel finder link 
        driver.get('https://www.vesselfinder.com/pro/map#vessel-details?imo={}'.format(vessel_imo))
        elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "app")))
   
        # pause 0.1s     
        if i == 0:
            time.sleep(10)
        else:
            time.sleep(0.5)
                    
        # pull page source
        source = driver.page_source
      
        # pause 0.1s
        if i == 0:
            time.sleep(10)
        else:
            time.sleep(0.5) 
        
        #set vessel score to 0
        vessel_score = 0
        number_trial = 1
        
        while vessel_score < 15 and number_trial <= 3: #15 out of 25 features must be available
            
            # pause 0.1s
            if i == 0:
                time.sleep(5)
            else:
                time.sleep(0.5) 
            
            #set vessel score to 0
            vessel_score = 0 
            
            # pull data from source
            try:
                vessel_type = source.split('<div class="oJ4cc">')[1].split(',')[0]
                vessel_score = vessel_score + 1
            except: 
                vessel_type = 'No data'
            try:   
                vessel_name = source.split('<h1 class="_3q1Jl">')[1].split('<!')[0]
                vessel_score = vessel_score + 1
            except:
                vessel_name = 'No data' 
            try:
                status = source.split('<div class="_2p4wu hLD3S">')[1].split('<!')[0].strip() 
                vessel_score = vessel_score + 1
            except: 
                status = 'No data'
            try:
                lat = source.split('<div class="coordinate lat">')[1].split('</div>')[0]
                vessel_score = vessel_score + 1
            except: 
                lat = 'No data'
            try:   
                lon = source.split('<div class="coordinate lon">')[1].split('</div>')[0]
                vessel_score = vessel_score + 1
            except:
                lon = 'No data'
            try:
                position_received = source.split('Position received')[1].split('ago')[0].split('<div>')[1].strip()
                vessel_score = vessel_score + 1
            except: 
                position_received = 'No data'
            try:
                navigation_status = source.split('Navigation Status')[1].split('ago')[0].split('<div>')[1].strip()
                vessel_score = vessel_score + 1
            except: 
                navigation_status = 'No data'
            try:
                ata_utc = source.split('ATA')[1].split('UTC')[0].split('>:')[1].split('<!')[0].strip()   
                vessel_score = vessel_score + 1
            except:
                ata_utc = 'No data'
            try:
                atd_utc = source.split('ATD')[1].split('UTC')[0].split('>:')[1].split('<!')[0].strip()
                vessel_score = vessel_score + 1
            except:
                atd_utc = 'No data'
            try:
                eta_utc = source.split('ETA')[1].split('UTC')[0].split('>:')[1].split('<!')[0].strip()
                vessel_score = vessel_score + 1
            except: 
                eta_utc = 'No data'
            try:
                 destination_port_city = source.split('<div class="Znd6C"><span>')[1].split('<!---')[0].strip()   
                 vessel_score = vessel_score + 1
            except:
                 destination_port_city = 'No data'  
            try:
                 destination_port_country = source.split('<div class="Znd6C"><span>')[1].split('<!---')[1].split('-->, ')[1].strip()    
                 vessel_score = vessel_score + 1
            except:
                 destination_port_country = 'No data'  
            try:
                 origin_port_city = source.split('<div class="Znd6C"><span>')[2].split('<!---')[0].strip()   
                 vessel_score = vessel_score + 1
            except:
                 origin_port_city = 'No data'  
            try:
                 origin_port_country = source.split('<div class="Znd6C"><span>')[2].split('<!---')[1].split('-->, ')[1].strip()   
                 vessel_score = vessel_score + 1
            except:
                 origin_port_country = 'No data'  
            try:
                course_degree = source.split('Course / Speed')[1].split('kn')[0].split('">')[1].split('/')[0].strip()
                vessel_score = vessel_score + 1
            except:
                course_degree =' No data'
            try:
                speed_kn = source.split('Course / Speed')[1].split('kn')[0].split('">')[1].split('/')[1].strip()
                vessel_score = vessel_score + 1
            except: 
                speed_kn = 'No data'
            try:
                length_meters = source.split('Length / Beam')[1].split('kn')[0].split('">')[1].split('/')[0].strip()
                vessel_score = vessel_score + 1
            except:
                length_meters = 'No data'
            try:
                beam_meters = source.split('Length / Beam')[1].split('m')[0].split('">')[1].split('/')[1].strip()
                vessel_score = vessel_score + 1
            except:
                beam_meters = 'No data'
            try:
                temperature_f = source.split('°F')[0].split('"_1HM6b">')[1].strip()
                vessel_score = vessel_score + 1
            except:
                temperature_f = 'No data'
            try:
                temperature_c = source.split('°C')[0].split('"_1GgDV">')[1].strip()
                vessel_score = vessel_score + 1
            except: 
                temperature_c = 'No data'
            try:
                wind_speed_ms = source.split('m/s')[0].split('"_1HM6b">')[2].strip()
                vessel_score = vessel_score + 1
            except:
                wind_speed_ms = 'No data'
            try:   
                wind_speed_kn = source.split('kn')[1].split('"_1GgDV">')[2].strip()
                vessel_score = vessel_score + 1
            except:
                wind_speed_kn = 'No data'
            try:
                sea_height_meters = source.split('m<')[2].split('<div class="_1GgDV">')[3].strip()
                vessel_score = vessel_score + 1
            except: 
                sea_height_meters = 'No data'
            try:
                sea_height_feet = source.split('ft<')[0].split('<div class="_1HM6b">')[3].strip() 
                if len(sea_height_feet) < 10:
                    vessel_score = vessel_score + 1
                else:
                    sea_height_feet = 'No data'
            except: 
                sea_height_feet = 'No data'
            try:
                status = source.split('<div class="_2p4wu hLD3S">')[1].split('<!')[0].strip() 
                vessel_score = vessel_score + 1
            except: 
                status = 'No data'
            try:
                remaining_distance_nautic_miles = source.split('<div class="_2p4wu _146U-"><div>')[2].split('nm')[0].strip() 
                vessel_score = vessel_score + 1
            except: 
                remaining_distance_nautic_miles = 'No data'
            try:
                remaining_time = source.split('<div class="_2p4wu _146U-"><div>')[2].split('<!')[1].split('/')[1].strip() 
                vessel_score = vessel_score + 1       
            except: 
                remaining_time = 'No data'
            try:
                port_name_call_1 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_name_call_1 = 'No data'
            try:
                port_country_call_1 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[1].split('<!---')[1].split('-->, ')[1].strip() 
                #vessel_score = vessel_score + 1
            except:
                port_country_call_1 = 'No data'
            try:
                port_arrival_call_1 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Arrival (UTC)</div>')[1].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_arrival_call_1 = 'No data'
            try:
                port_departure_call_1 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Departure (UTC)</div>')[1].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_departure_call_1 = 'No data' 
            try:
                in_port_call_1 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">In Port</div>')[1].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                in_port_call_1 = 'No data' 
            try:
                port_name_call_2 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[2].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_name_call_2 = 'No data'
            try:
                port_country_call_2 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[2].split('<!---')[1].split('-->, ')[1].strip() 
                #vessel_score = vessel_score + 1
            except:
                port_country_call_2 = 'No data'
            try:
                port_arrival_call_2 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Arrival (UTC)</div>')[2].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_arrival_call_2 = 'No data'
            try:
                port_departure_call_2 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Departure (UTC)</div>')[2].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_departure_call_2 = 'No data' 
            try:
                in_port_call_2 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">In Port</div>')[2].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                in_port_call_2 = 'No data' 
            try:
                port_name_call_3 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[3].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_name_call_3 = 'No data'
            try:
                port_country_call_3 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[3].split('<!---')[1].split('-->, ')[1].strip() 
                #vessel_score = vessel_score + 1
            except:
                port_country_call_3 = 'No data'
            try:
                port_arrival_call_3 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Arrival (UTC)</div>')[3].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_arrival_call_3 = 'No data'
            try:
                port_departure_call_3 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Departure (UTC)</div>')[3].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_departure_call_3 = 'No data' 
            try:
                in_port_call_3 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">In Port</div>')[3].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                in_port_call_3 = 'No data'   
            try:
                port_name_call_4 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[4].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_name_call_4 = 'No data'
            try:
                port_country_call_4 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[4].split('<!---')[1].split('-->, ')[1].strip() 
                #vessel_score = vessel_score + 1
            except:
                port_country_call_4 = 'No data'
            try:
                port_arrival_call_4 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Arrival (UTC)</div>')[4].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_arrival_call_4 = 'No data'
            try:
                port_departure_call_4 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Departure (UTC)</div>')[4].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_departure_call_4 = 'No data' 
            try:
                in_port_call_4 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">In Port</div>')[4].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                in_port_call_4 = 'No data'  
            try:
                port_name_call_5 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[5].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_name_call_5 = 'No data'
            try:
                port_country_call_5 = source.split('Recent Port Calls')[1].split('svg&quot;);"></span>')[5].split('<!---')[1].split('-->, ')[1].strip() 
                #vessel_score = vessel_score + 1
            except:
                port_country_call_5 = 'No data'
            try:
                port_arrival_call_5 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Arrival (UTC)</div>')[5].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_arrival_call_5 = 'No data'
            try:
                port_departure_call_5 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">Departure (UTC)</div>')[5].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                port_departure_call_5 = 'No data' 
            try:
                in_port_call_5 = source.split('Recent Port Calls')[1].split('<div class="_2nufK">In Port</div>')[5].split('<div class="_1GQkK">')[1].split('<!---')[0].strip() 
                #vessel_score = vessel_score + 1
            except: 
                in_port_call_5 = 'No data'  
                
            print(str(number_trial) + ' ' + status)
            
            number_trial = number_trial + 1

            # update some fiels 
            # if the ship is moored there is no ETA and ATD
            if status == 'Moored':
                eta_utc = 'No data'
                atd_utc = 'No data'
            # if the ship is moored there is not lat/lng 
         
            if status == 'Moored':          
                try:
                    lat = port_data_dic[destination_port_city][0][0]
                    lon = port_data_dic[destination_port_city][0][1]
                except:
                    lat = 'No data'    
                    lon = 'No data'
                
            if position_received[0:8] == 'just now':
                position_received = '0 mins'

            if len(temperature_f) > 10:
                temperature_f = 'No data'
            if len(temperature_c) > 10:
                temperature_c = 'No data'       
            if len(wind_speed_ms) > 10:
                wind_speed_ms = 'No data'
            if len(wind_speed_ms) > 10:
                wind_speed_ms = 'No data'
            if len(wind_speed_kn) > 10:
                wind_speed_kn = 'No data'
            if len(sea_height_meters) > 10:
                sea_height_meters = 'No data'
            if len(sea_height_feet) > 10:
                sea_height_feet = 'No data'
            if len(sea_height_feet) > 10:
                sea_height_feet = 'No data'
            if len(remaining_distance_nautic_miles) > 10:
                remaining_distance_nautic_miles = 'No data'
            if len(remaining_time) > 10:
                remaining_time = 'No data'
                
            if sea_height_meters == 'No data' and sea_height_feet != 'No data':
                sea_height_meters = str(float(sea_height_feet)  * 0.3048)
    
        # only add data to file if number of trial is less than 5 and status is not null
        if number_trial <=3 and status != 'No data':
          
            #print(port_arrival_call_1)
            #print(port_departure_call_1)
            #print(in_port_call_1)
            #print(port_name_call_1)
            
            # create lists
            List_first_name = [] 
            List_last_name = [] 
            List_email = [] 
            List_imo = []   
            List_vessel_type = []
            List_vessel_name = []
            List_lat = []
            List_lon = []
            List_position_received = []
            List_navigation_status = []
            List_origin_port_city = []
            List_destination_port_city = []
            List_origin_port_country = []
            List_destination_port_country = []
            List_ata_utc = []
            List_atd_utc = []
            List_eta_utc = []
            List_course_degree = []
            List_speed_kn = []
            List_length_meters = []
            List_beam_meters = []
            List_temperature_f = []
            List_temperature_c = []
            List_wind_speed_ms = []
            List_wind_speed_kn = []
            List_sea_height_meters = []
            List_sea_height_feet = []
            List_status = []
            List_remaining_distance_nautic_miles = []
            List_remaining_time = []
            List_current_time_utc = []
            List_port_name_call_1 = []
            List_port_country_call_1 = []
            List_port_arrival_call_1 = []
            List_port_departure_call_1 = []
            List_in_port_call_1 = []
            List_in_port_call_2 = []
            List_port_name_call_2 = []
            List_port_country_call_2 = []
            List_port_arrival_call_2 = []
            List_port_departure_call_2 = []
            List_in_port_call_2 = []
            List_port_name_call_3 = []
            List_port_country_call_3 = []
            List_port_arrival_call_3 = []
            List_port_departure_call_3 = []
            List_in_port_call_3 = []
            List_port_name_call_4 = []
            List_port_country_call_4 = []
            List_port_arrival_call_4 = []
            List_port_departure_call_4 = []
            List_in_port_call_4 = []
            List_port_name_call_5 = []
            List_port_country_call_5 = []
            List_port_arrival_call_5 = []
            List_port_departure_call_5 = []
            List_in_port_call_5 = []
       
            # add data to lists
            List_first_name.append(first_name)
            List_last_name.append(last_name)
            List_email.append(email)
            List_imo.append(vessel_imo)
            List_vessel_type.append(vessel_type)
            List_vessel_name.append(vessel_name)
            List_lat.append(lat)
            List_lon.append(lon)
            List_position_received.append(position_received)
            List_navigation_status.append(navigation_status)
            List_origin_port_city.append(origin_port_city)
            List_destination_port_city.append(destination_port_city)
            List_origin_port_country.append(origin_port_country)
            List_destination_port_country.append(destination_port_country)
            List_ata_utc.append(ata_utc)
            List_atd_utc.append(atd_utc)
            List_eta_utc.append(eta_utc)
            List_course_degree.append(course_degree)
            List_speed_kn.append(speed_kn)
            List_length_meters.append(length_meters)
            List_beam_meters.append(beam_meters)
            List_temperature_f.append(temperature_f)
            List_temperature_c.append(temperature_c)
            List_wind_speed_ms.append(wind_speed_ms)
            List_wind_speed_kn.append(wind_speed_kn)
            List_sea_height_meters.append(sea_height_meters)
            List_sea_height_feet.append(sea_height_feet)
            List_status.append(status)
            List_remaining_distance_nautic_miles.append(remaining_distance_nautic_miles)
            List_remaining_time.append(remaining_time)
            List_current_time_utc.append(current_time_utc)
            List_port_name_call_1.append(port_name_call_1)
            List_port_country_call_1.append(port_country_call_1)
            List_port_arrival_call_1.append(port_arrival_call_1)
            List_port_departure_call_1.append(port_departure_call_1)
            List_in_port_call_1.append(in_port_call_1)
            List_port_name_call_2.append(port_name_call_2)
            List_port_country_call_2.append(port_country_call_2)
            List_port_arrival_call_2.append(port_arrival_call_2)
            List_port_departure_call_2.append(port_departure_call_2)
            List_in_port_call_2.append(in_port_call_2)
            List_port_name_call_3.append(port_name_call_3)
            List_port_country_call_3.append(port_country_call_3)
            List_port_arrival_call_3.append(port_arrival_call_3)
            List_port_departure_call_3.append(port_departure_call_3)
            List_in_port_call_3.append(in_port_call_3)               
            List_port_name_call_4.append(port_name_call_4)
            List_port_country_call_4.append(port_country_call_4)
            List_port_arrival_call_4.append(port_arrival_call_4)
            List_port_departure_call_4.append(port_departure_call_4)
            List_in_port_call_4.append(in_port_call_4)
            List_port_name_call_5.append(port_name_call_5)
            List_port_country_call_5.append(port_country_call_5)
            List_port_arrival_call_5.append(port_arrival_call_5)
            List_port_departure_call_5.append(port_departure_call_5)
            List_in_port_call_5.append(in_port_call_5)
            
            # create dataframe
            new_data = {'first_name' : List_first_name, 'last_name' : List_last_name, 'email' : List_email, 'vessel_type' : List_vessel_type, 'vessel_name' : List_vessel_name, 'imo' : List_imo, 'status' : List_status, 'lat' : List_lat, 'lon' : List_lon, 'position_received' : List_position_received, 'origin_port_city' : List_origin_port_city,'origin_port_country' : List_origin_port_country, 'destination_port_city' : List_destination_port_city,'destination_port_country;' : List_destination_port_country, 'ATA' : List_ata_utc, 'ATD' : List_atd_utc, 'ETA' : List_eta_utc, 'course_degree' : List_course_degree, 'speed_kn' : List_speed_kn, 'length_meters' : List_length_meters, 'beam_meters' : List_beam_meters, 'temperature_farenheiht' : List_temperature_f, 'temperature_celsius' : List_temperature_c,'wind_speed_ms' : List_wind_speed_ms, 'sea_height_meters': List_sea_height_meters, 'distance_nautic_miles' : List_remaining_distance_nautic_miles, 'time' : List_remaining_time,'in_port_name_call_1' : List_port_name_call_1,'in_port_country_call_1' : List_port_country_call_1, 'port_arrival_call_1' : List_port_arrival_call_1, 'port_departure_call_1' : List_port_departure_call_1, 'in_port_call_1' : List_in_port_call_1,'in_port_name_call_2' : List_port_name_call_2,'in_port_country_call_2' : List_port_country_call_2, 'port_arrival_call_2' : List_port_arrival_call_2, 'port_departure_call_2' : List_port_departure_call_2, 'in_port_call_2' : List_in_port_call_2,'in_port_name_call_3' : List_port_name_call_3,'in_port_country_call_3' : List_port_country_call_3, 'port_arrival_call_3' : List_port_arrival_call_3, 'port_departure_call_3' : List_port_departure_call_3, 'in_port_call_3' : List_in_port_call_3,'in_port_name_call_4' : List_port_name_call_4,'in_port_country_call_4' : List_port_country_call_4, 'port_arrival_call_4' : List_port_arrival_call_4, 'port_departure_call_4' : List_port_departure_call_4, 'in_port_call_4' : List_in_port_call_4, 'in_port_name_call_5' : List_port_name_call_5,'in_port_country_call_5' : List_port_country_call_5, 'port_arrival_call_5' : List_port_arrival_call_5, 'port_departure_call_5' : List_port_departure_call_5, 'in_port_call_5' : List_in_port_call_5,'current_time_utc' : current_time_utc}
            df_new = pd.DataFrame(new_data)               
            
            # check if output file exists for this customer
            # if yes add new data to old data
            # if no create a new output file and inseet new data
            try:
                df_old = pd.read_excel('Output_{}_{}.xlsx'.format(first_name,last_name))
                df_new = pd.concat([df_old, df_new])
                df_new.to_excel('Output_{}_{}.xlsx'.format(first_name,last_name), index=False)
                print('output file already exists for this customer')
            except:
                df_new.to_excel('Output_{}_{}.xlsx'.format(first_name,last_name),index=False)
                print('no output file for this customer')
        
            #write text file
            if i <=2:
                with open('readme_{}.txt'.format(i), 'w') as f:
                    f.write(source)
        
    # quite driver
    driver.quit()
        
