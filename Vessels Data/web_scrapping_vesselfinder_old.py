# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 09:59:47 2021

@author: TXF10LQ
"""



## import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#import others packages
from os import listdir
from os.path import isfile, join
import time
import pandas as pd
from bs4 import BeautifulSoup

## import google packages
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
from google.api_core import retry
import time
import os 
from datetime import date as dt
from datetime import datetime as dtime



today = dt.today()
print("Today's date:", today)



print('Vessel data pull')
#pull estimated final cy dates (POs are already ranked with FIFO)
query_1 = '''
select * from (
select distinct 
case when vessel like '%COSCO SHIPPIGN%' then replace(replace(vessel,'SHIPPING',''),'  ',' ') else vessel end vessel 
from `analytics-supplychain-thd.INTLOPS.IL_Lead_Time_PO_Level`
where po_status = 'PS') 
where vessel is not null '''

retry_param = retry.Retry(deadline = 30)
client = bigquery.Client(project = 'analytics-supplychain-thd', location = 'US')
query = query_1

data =  client.query(query, retry = retry_param).result().to_dataframe()

print('Define lists')
#define lists
L_vessel = []
L_ais_type=[]
L_flag=[]
L_destination=[]
L_eta=[]
L_imo=[]
L_mmsi=[]
L_callsign=[]
L_length=[]
L_beam=[]
L_current_draught=[]
L_course =[]
L_speed =[]
L_lat=[]
L_long=[]
L_status = []
L_position_received = []
L_partition_datetime = []

count = 0 
failure = 0

driver = webdriver.Chrome('C:\\Users\TXF10LQ\\OneDrive - The Home Depot\\Documents\\Work\\Python Codes Fancy\\LTL_Report\\chromedriver.exe')

print('Webscrapping starts')
#start webscrapping 
for vessel in data['vessel']:
    
    print('Start {}'.format(vessel))
    string = vessel
    ##driver = webdriver.PhantomJS('C:\\Users\TXF10LQ\\OneDrive - The Home Depot\\Documents\\Work\\Python Codes Fancy\\LTL_Report\\phantomjs.exe')
    #driver = webdriver.Edge('C:\\Users\TXF10LQ\\OneDrive - The Home Depot\\Documents\\Work\\Python Codes Fancy\\LTL_Report\\msedgedriver2.exe')
    #driver = webdriver.Ie('C:\\Users\TXF10LQ\\OneDrive - The Home Depot\\Documents\\Work\\Python Codes Fancy\\LTL_Report\\IEDriverServer.exe')
    driver.set_window_position(-10000,0)
    print('Search for website')
    fileinput = driver.get("https://www.vesselfinder.com/vessels?name={}".format(string))
    #time.sleep(0.05)
    print('Find ship id : ship_name + IMO + MMSI')
    
    try:

        fileinput = driver.find_element_by_class_name('ship-link').get_attribute("href")
        #time.sleep(0.05)
        fileinput_split = fileinput.split('/')
        unique_id = fileinput_split[len(fileinput_split)-1]
        print('search for ship coordinates')
        fileinput_coordinates = driver.get("https://www.vesselfinder.com/vessels/{}".format(unique_id))
        #time.sleep(0.05)
        #print('method1')
        #get the text (better solution would be to pull data from table but i have not found a way to do that yet)
        #text = driver.find_element_by_class_name('text2').text
        #table = driver.find_elements_by_xpath("//table/tbody/tr[2]/td")
        #print(text)
        fileinput = driver.page_source
        #driver.close()
    
        #print('method2')
        #hardcoding not the best again but this works for now
        ##just grab position, eta and position received for now since they changed the html
        lat_1 = fileinput.split('Lat:</div><div class="coordinate lat">')[1]
        lat_2 = lat_1.split('</div>')[0]
        
        long_1 = fileinput.split('Lon:</div><div class="coordinate lon">')[1]
        long_2 = long_1.split('</div>')[0]
        
        try:
            ETA_1 = fileinput.split('<span class="_mcol12">ETA:')[1]
            ETA_2 = ETA_1.split('</span><span class="_arrLb"></span>')[0].lstrip()

        except:
            ETA_2 = 'Null'
        
                
        try:
            try:
                Last_Position_1 = fileinput.split('id="lastrep"><span class="">')[1]
                Last_Position_2 = Last_Position_1.split('</span> <span class="info"><i>i</i></span></td>')[0].lstrip()
            except:
                Last_Position_1 = fileinput.split('id="lastrep"><span class="red">')[1]
                Last_Position_2 = Last_Position_1.split('</span> <span class="info"><i>i</i></span></td>')[0].lstrip()   
        except:
             Last_Position_2 = 'Null'
             
            
        
        print(ETA_2)
        print(Last_Position_2)
    
        data_frame = 'null'
        
        now = dtime.now()   
        dt_string = now.strftime("%d/%m/%Y %H:%M")
        print("Date and time =", dt_string)	
        print(count)
        
 

        L_vessel.append(vessel)

        L_ais_type.append("NA")

        L_flag.append("NA")

        L_destination.append("NA")
        
        try:
            L_eta.append(ETA_2)
        except:
            L_eta.append("NA")

        L_imo.append("NA")

        L_mmsi.append("NA")

        L_callsign.append("NA")

        L_length.append("NA")

        L_beam.append("NA")

        L_current_draught.append("NA")

        L_course.append("NA")

        L_speed.append("NA")
        
        try:
            L_long.append(long_2)
        except:
            L_long.append("NA")
        try:
            L_lat.append(lat_2)
        except:
            L_lat.append("NA")
            
        L_status.append("NA")
        
        try:
            L_position_received.append(Last_Position_2)
        except:
            L_position_received.append("NA")
        try:
            L_partition_datetime.append(dt_string)
        except:
            L_partition_datetime.append("NA")
        
        print('{} succeeded'.format(string))
        print(lat_2)
        print(long_2)
        count = count + 1

        
    except:
        print('{} failed web scrapping'.format(string))
        failure = failure + 1
   



#straight upload to the raw vessel locations data - insert
data_table = {'Vessel' : L_vessel, 'AIS_Type':L_ais_type, 'Flag' : L_flag,'Destination' : L_destination, 'ETA':L_eta, 'IMO' : L_imo, 'MMSI' : L_mmsi,'Callsign':L_callsign,'Length':L_length, 'Beam' : L_beam,'Current_Draught':L_current_draught,'Course':L_course,'Speed' : L_speed,'Lat':L_lat,'Long':L_long,'Status':L_status,'Position_Received':L_position_received,'Partition_Date':L_partition_datetime}
new_dataframe = pd.DataFrame(data=data_table)
new_dataframe.to_gbq('INTLOPS.VESSEL_FINDER_ARCHIVE_DATA',project_id = 'analytics-supplychain-thd',if_exists='append')  



#clean and insert data into BQ table for PS POs
query_1 = '''
insert into `analytics-supplychain-thd.INTLOPS.PO_VESSEL_TRACKING_IMPORT` 
select * from (
select 
a.po,
a.po_create_date,
a.po_type,
a.confirmed_flg_check,
a.po_status as po_status,
a.program_name,
a.mode,
a.dept,
a.contract_flg,
a.feu,
a.factory_id,
a.vessel,
a.carrier,
a.mvndr_nbr,
a.origin_country,
a.port_of_origin,
a.port_of_destination,
a.port_of_destination_name,
a.final_cy,
a.final_cy_name,
a.dc_nbr,
a.dc_name,
a.dc_type,
estimated_vessel_arrival,
estimated_port_available,
estimated_port_departure,
estimated_dc_delivery,
estimated_dc_keyrec,
replace(replace(case when b.lat like '%S%' then concat('-',b.lat) else b.lat  end,'S',''),'N','') lat,
replace(replace(case when b.long like '%W%'then concat('-',b.long) else b.long  end,'W',''),'E','') long,
case when eta = '-' then null else eta end as eta,
case when course = '-' then null else course end as course,
case when speed = '-' then null else speed end as speed,
b.position_received, 
b.ais_type,
cast(concat(substr(left(b.partition_date ,10),7,10),'-',substr(left(b.partition_date ,10),4,2),'-',substr(left(b.partition_date ,10),1,2)) as date) partition_date
from `analytics-supplychain-thd.INTLOPS.IL_Lead_Time_PO_Level` a
left join `analytics-supplychain-thd.INTLOPS.VESSEL_FINDER_ARCHIVE_DATA` b
on a.vessel = b.vessel
where po_flag = 'Yes' and vessel_arrival is null and vessel_departure is not null)
where partition_date = current_date()'''



retry_param = retry.Retry(deadline = 30)
client = bigquery.Client(project = 'analytics-supplychain-thd', location = 'US')
query = query_1

data =  client.query(query, retry = retry_param).result().to_dataframe()






