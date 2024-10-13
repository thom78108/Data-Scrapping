#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon May 15 10:32:24 2023

@author: elizabethtnguyen
"""

#from multiprocessing import Process



#def main(var,number_cities_start,number_cities_end,x):
     
var = True 
number_cities_start = 0 
number_cities_end = 10
x = 0

#import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
        
#define N
N = 0 

#list failed cities
list_failures = []

#import top us cities and define functions/variables
if var == True:
    
    print('start import top us cities')

    #define lists
    list_population = []
    list_city = []
    list_state = []
    list_state_v2 = []
    list_city_state = []
    list_city_state_v2 = []
    
    #index from 1 to 10 to cover all pages on the website
    for index in range(1,11):
       
        #request access and pull html
        a = requests.get("https://www.biggestuscities.com/{}".format(index))
        soup = BeautifulSoup(a.text, features = 'lxml')
        tables = soup.findAll('table', 'table-condensed')
    
        
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
    
        #find cities and states in html
        for table in tables:
            for row in table.findAll("tr")[0:]:
                cols = row.findAll('td')
                if len(cols) > 2:
                    list_city.append(cols[1].text.split('href')[0].split(',')[0].lstrip())
                    list_state.append(cols[1].text.split('href')[0].split(',')[1].lstrip()[:2])
                    list_state_v2.append(abbrev_to_us_state[cols[1].text.split('href')[0].split(',')[1].lstrip()[:2]])
                    list_city_state.append(cols[1].text.split('href')[0].split(', ')[0].lstrip() + ", " + cols[1].text.split('href')[0].split(',')[1].lstrip()[:2])
                    list_city_state_v2.append(cols[1].text.split('href')[0].split(', ')[0].lstrip() + ", " + abbrev_to_us_state[cols[1].text.split('href')[0].split(',')[1].lstrip()[:2]])
                    list_population.append(cols[2].text.split('href')[0].split(', ')[0].lstrip())
                    
    print('end import top us cities')

#rename some cities manually to allow data scrapping
list_city[20] = 'Nashville-Davidson'
list_city[58] = 'Lexington-Fayette'
list_city[93] = 'Boise'
list_city[164] = 'Macon'

#define driver to webscrap data

#define options selenium
options = Options()
options.headless = True

#define driver
service = Service(executable_path='/Users/thomasfrancois/Desktop/chromedriver_v1')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
#driver.set_window_position(0,0)
#driver.set_window_size(0,0)

#loop on the top 1000 cities
for i in range(number_cities_start,number_cities_end):
    
    
    try: 
        
        print(list_city_state[i])
        print(i)
        
        #### PART 1 IMPORT CLIMATE TOP 1000 US CITIES ##### Source = bestplace.net 
        if var == True:
                
            print('start import climate data')
            
            #define lists data
            list_rainfall = []
            list_snowfall = []
            list_average_rainy_days = []
            list_average_sunny_days = []
            list_average_high_jul = []
            list_average_low_jan = []
            list_comfort_index = []
            list_uv_index = []
            list_elevation = []
            
            #define lists definition
            list_rainfall_def = []
            list_snowfall_def = []
            list_average_rainy_days_def = []
            list_average_sunny_days_def = []
            list_average_high_jul_def = []
            list_average_low_jan_def = []
            list_comfort_index_def = []
            list_uv_index_def = []
            list_elevation_def = []
            
            
            #pull html with selenium
            driver.get("https://www.bestplaces.net/climate/city/{}/{}".format(list_state_v2[i],list_city[i]))
         
            #pull weather data
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[2]/td[2]"):
                    list_rainfall.append(convert_str_to_float(element.get_attribute("innerText")))                    
            except:
                list_rainfall.append(None)
            
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[3]/td[2]"):
                    list_snowfall.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_snowfall.append(None)
           
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[4]/td[2]"):
                    list_average_rainy_days.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_average_rainy_days.append(None)
            
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[5]/td[2]"):
                    list_average_sunny_days.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_average_sunny_days.append(None)
                
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[6]/td[2]"):
                    list_average_high_jul.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_average_high_jul.append(None)
            
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[7]/td[2]"):
                    list_average_low_jan.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_average_low_jan.append(None)
         
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[8]/td[2]"):
                    list_comfort_index.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_comfort_index.append(None)
            
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[9]/td[2]"):
                    list_uv_index.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_uv_index.append(None)
            
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[10]/td[2]"):
                    list_elevation.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_elevation.append(None)
                                     
            #pull definitions    
            if i == 0:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[2]/td[1]/button"):
                    list_rainfall_def.append(element.get_attribute('data-original-title')) 
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[3]/td[1]/button"):
                    list_snowfall_def.append(element.get_attribute('data-original-title')) 
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[4]/td[1]/button"):
                    list_average_rainy_days_def.append(element.get_attribute('data-original-title'))                         
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[5]/td[1]/button"):
                    list_average_sunny_days_def.append(element.get_attribute('data-original-title'))     
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[6]/td[1]/button"):
                    list_average_high_jul_def.append(element.get_attribute('data-original-title'))                             
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[7]/td[1]/button"):
                    list_average_low_jan_def.append(element.get_attribute('data-original-title'))                          
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[8]/td[1]/button"):
                    list_comfort_index_def.append(element.get_attribute('data-original-title')) 
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[9]/td[1]/button"):
                    list_uv_index_def.append(element.get_attribute('data-original-title')) 
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgClimate']/tbody/tr[10]/td[1]/button"):
                    list_elevation_def.append(element.get_attribute('data-original-title')) 
                    
            print('end import climate data')
        
    
        #### PART 2 IMPORT COST DATA #### Source = bestplace.net
        if var == True:
            
            print('start import cost data')
                
            #define lists data
            list_cost_of_living_overall = []
            list_cost_of_grocery = []
            list_cost_of_health = []
            list_cost_of_housing = []
            list_cost_of_median_home_cost = []
            list_cost_of_utilities = []
            list_cost_of_transportation = []
            list_cost_of_miscellanous = []

            #define lists definitions
            list_cost_of_living_overall_def = []
            list_cost_of_grocery_def = []
            list_cost_of_health_def = []
            list_cost_of_housing_def = []
            list_cost_of_median_home_cost_def = []
            list_cost_of_utilities_def = []
            list_cost_of_transportation_def = []
            list_cost_of_miscellanous_def = []
            
            #pull html with selenium
            driver.get("https://www.bestplaces.net/cost_of_living/city/{}/{}".format(list_state_v2[i],list_city[i]))
                
            #data
            try:
                #pull cost data
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[2]/td[2]"):
                    list_cost_of_living_overall.append(element.get_attribute("innerText"))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[3]/td[2]"):
                    list_cost_of_grocery.append(element.get_attribute("innerText"))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[4]/td[2]"):
                    list_cost_of_health.append(element.get_attribute("innerText"))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[5]/td[2]"):
                    list_cost_of_housing.append(element.get_attribute("innerText"))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[6]/td[2]"):
                    list_cost_of_median_home_cost.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[7]/td[2]"):
                    list_cost_of_utilities.append(element.get_attribute("innerText"))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[8]/td[2]"):
                    list_cost_of_transportation.append(element.get_attribute("innerText"))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[9]/td[2]"):
                    list_cost_of_miscellanous.append(element.get_attribute("innerText"))
                
                #print('cost data available')   
                
            except:
                list_cost_of_living_overall.append(None)
                list_cost_of_grocery.append(None)
                list_cost_of_health.append(None)
                list_cost_of_housing.append(None)
                list_cost_of_median_home_cost.append(None)
                list_cost_of_utilities.append(None)
                list_cost_of_transportation.append(None)
                list_cost_of_miscellanous.append(None)
                
                #print('cost data not available')
            
            #definitions
            if i == 0:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[2]/td[1]/u/button"):
                    list_cost_of_living_overall_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[3]/td[1]/u/button"):
                    list_cost_of_grocery_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[4]/td[1]/u/button"):
                    list_cost_of_health_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[5]/td[1]/u/button"):
                    list_cost_of_housing_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[6]/td[1]/u/button"):
                    list_cost_of_median_home_cost_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[7]/td[1]/u/button"):
                    list_cost_of_utilities_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[8]/td[1]/u/button"):
                    list_cost_of_transportation_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgCostOfLiving']/tbody/tr[9]/td[1]/u/button"):
                    list_cost_of_miscellanous_def.append(element.get_attribute('data-original-title'))
                                  
            print('end import cost data') 
            
        
        #### PART 3 IMPORT CRIME DATA #### Source = bestplace.net
        if var == True:
            
            print('start import crime data')
                
            #define lists data
            #violent crimes
            list_violent = []
            list_murder = []
            list_rape = []
            list_robbery = []
            list_assault = []
            #list property crimes
            list_property = []
            list_bulgary = []
            list_larceny = []
            list_auto = []
            #list indexes
            list_index_violent = []
            list_index_property = []
            
            #define lists definitions
            #violent crimes
            list_violent_def = []
            list_murder_def  = []
            list_rape_def  = []
            list_robbery_def  = []
            list_assault_def  = []
            #list property crimes
            list_property_def  = []
            list_bulgary_def  = []
            list_larceny_def  = []
            list_auto_def  = []
            #list indexes
            list_index_violent_def  = []
            list_index_property_def = []
            
            #pull html with selenium
            driver.get("https://www.bestplaces.net/crime/city/{}/{}".format(list_state_v2[i],list_city[i]))
            page_source = driver.page_source
            page_source_split = page_source.split("<tbody>")[1]
            
            year = 0
            
            try:
                page_source_split_v2 = page_source_split.split("2020")[1]
                page_source_split_v3 = page_source_split_v2.split("</td></tr>")[0]
                page_source_split_v4 = page_source_split_v3.split("</td><td>")
                year = 2020
            except:
                None
                #print('crime data 2020 not available')
           
            try:
                if year == 0:
                    page_source_split_v2 = page_source_split.split("2019")[1]
                    page_source_split_v3 = page_source_split_v2.split("</td></tr>")[0]
                    page_source_split_v4 = page_source_split_v3.split("</td><td>")
                    year = 2019
            except:
                None
                #print('crime data 2019 not available')
        
            try:
                if year == 0:
                    page_source_split_v2 = page_source_split.split("2018")[1]
                    page_source_split_v3 = page_source_split_v2.split("</td></tr>")[0]
                    page_source_split_v4 = page_source_split_v3.split("</td><td>")
                    year = 2018
            except:
                page_source_split_v4 = ["NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA"]
                #print('crime data 2018 not available')
             
            #pull crime data
            try:
                list_violent.append(page_source_split_v4[1])
            except:
                list_violent.append(None)
            try:
                list_murder.append(page_source_split_v4[2])
            except:
                list_murder.append(None)
            try:
                list_rape.append(page_source_split_v4[3])
            except:
                list_rape.append(None)
            try:
                list_robbery.append(page_source_split_v4[4])
            except:
                list_robbery.append(None)
            try:
                list_assault.append(page_source_split_v4[5])
            except:
                list_assault.append(None)
            try:
                list_property.append(page_source_split_v4[6])
            except:
                list_property.append(None)
            try:
                list_bulgary.append(page_source_split_v4[7])
            except:
                list_bulgary.append(None)
            try:
                list_larceny.append(page_source_split_v4[8])
            except:
                list_larceny.append(None)
            try:
                list_auto.append(page_source_split_v4[9])
            except:
                list_auto.append(None)
            
            #pull indexes for violent crimes and property crimes
            page_source_split = page_source.split("{} violent crime is ".format(list_city[i]))[1]
            list_index_violent.append(page_source_split[0:4])
            page_source_split = page_source.split("{} property crime is ".format(list_city[i]))[1]
            list_index_property.append(page_source_split[0:4])
            
            
            if i == 0:
                #define lists definitions
                #violent crimes
                list_violent_def.append("N/A")
                list_murder_def.append("N/A")
                list_rape_def.append("N/A")
                list_robbery_def.append("N/A")
                list_assault_def.append("N/A")
                #list property crimes
                list_property_def.append("N/A")
                list_bulgary_def.append("N/A")
                list_larceny_def.append("N/A")
                list_auto_def.append("N/A")
                #list indexes
                list_index_violent_def.append("N/A")
                list_index_property_def.append("N/A")
            
        
        #### PART 4 IMPORT EDUCATION DATA #### Source = bestplace.net 
        if var == True:
            
            print('start education data')
                
            #define lists data
            #main metrics
            list_overall_expenses_per_student = []
            list_education_expenses_per_student = []
            list_instruction_expenses_per_student = []
            list_student_per_teacher = []
            list_students_per_librarian = []
            list_students_per_counselor = []
            #education distribution
            list_education_distribution = []
            list_grade_school = []
            list_some_high_school = []
            list_high_school_grad = []               
            list_high_school_grad_only = [] 
            list_some_college = [] 
            list_degree_two_years = [] 
            list_degree_four_years = [] 
            list_degree_four_year_only = [] 
            list_degree_masters = [] 
            list_degree_professional = [] 
            
            #define lists definitions
            #main metrics
            list_overall_expenses_per_student_def = []
            list_education_expenses_per_student_def = []
            list_instruction_expenses_per_student_def = []
            list_student_per_teacher_def = []
            list_students_per_librarian_def = []
            list_students_per_counselor_def = []
            #education distribution
            list_grade_school_def = []
            list_some_high_school_def = []
            list_high_school_grad_def = []               
            list_high_school_grad_only_def = [] 
            list_some_college_def = [] 
            list_degree_two_years_def = [] 
            list_degree_four_years_def = [] 
            list_degree_four_year_only_def = [] 
            list_degree_masters_def = [] 
            list_degree_professional_def = [] 
        
            
            #pull html with selenium
            driver.get("https://www.bestplaces.net/education/city/{}/{}".format(list_state_v2[i],list_city[i]))
            
            #pull education data
            try:
               for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[2]/td[2]"):
                   list_overall_expenses_per_student.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_overall_expenses_per_student.append(None)
            try:
               for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[3]/td[2]"):
                   list_education_expenses_per_student.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_education_expenses_per_student.append(None)
            try:
               for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[4]/td[2]"):
                   list_instruction_expenses_per_student.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_instruction_expenses_per_student.append(None)
            try:
               for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[5]/td[2]"):
                   list_student_per_teacher.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_student_per_teacher.append(None)
            try:
               for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[6]/td[2]"):
                   list_students_per_librarian.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_students_per_librarian.append(None)
            try:
               for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[7]/td[2]"):
                   list_students_per_counselor.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_students_per_counselor.append(None)

            
            #education distribution
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[3]/div/div/div[2]/script"):
                    list_education_distribution = element.get_attribute("innerHTML").split('data: ')[1].split(" }")[0].split(",")
                    list_grade_school.append(list_education_distribution[0].replace("[",''))         
                    list_some_high_school.append(list_education_distribution[1])       
                    list_high_school_grad.append(list_education_distribution[2])       
                    list_high_school_grad_only.append(list_education_distribution[3])       
                    list_some_college.append(list_education_distribution[4])       
                    list_degree_two_years.append(list_education_distribution[5])       
                    list_degree_four_years.append(list_education_distribution[6])       
                    list_degree_four_year_only.append(list_education_distribution[7])       
                    list_degree_masters.append(list_education_distribution[8])       
                    list_degree_professional.append(list_education_distribution[9].replace("]",''))       
            except:
                    list_grade_school.append(None)     
                    list_some_high_school.append(None)        
                    list_high_school_grad.append(None)    
                    list_high_school_grad_only.append(None)        
                    list_some_college.append(None)         
                    list_degree_two_years.append(None)       
                    list_degree_four_years.append(None)     
                    list_degree_four_year_only.append(None)     
                    list_degree_masters.append(None)       
                    list_degree_professional.append(None)        
            
            
            if i == 0:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[2]/td[1]/button"):
                    list_overall_expenses_per_student_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[3]/td[1]/button"):
                    list_education_expenses_per_student_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[4]/td[1]/button"):
                    list_instruction_expenses_per_student_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[5]/td[1]/button"):
                    list_student_per_teacher_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[6]/td[1]/button"):
                    list_students_per_librarian_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEducation']/tbody/tr[7]/td[1]/button"):
                    list_students_per_counselor_def.append(element.get_attribute('data-original-title'))
                    

                list_grade_school_def.append("N/A")        
                list_some_high_school_def.append("N/A")       
                list_high_school_grad_def.append("N/A")      
                list_high_school_grad_only_def.append("N/A")       
                list_some_college_def.append("N/A")       
                list_degree_two_years_def.append("N/A")        
                list_degree_four_years_def.append("N/A")        
                list_degree_four_year_only_def.append("N/A")         
                list_degree_masters_def.append("N/A")        
                list_degree_professional_def.append("N/A")   
                
            print('end education data')
        
        #### PART 5 IMPORT ECONOMY DATA #### Source = bestplace.net 
        if var == True:
            
            print('start economy data')
                
            #define lists data
            #main metrics
            list_umemployment_rate = []
            list_recent_job_growth = []
            list_future_job_growth = []
            list_sales_taxes = []
            list_income_tax = []
            list_income_per_capita = []
            list_household_income = []
            list_family_median_income = []
            #income distribution 
            list_income_distribution = []
            list_under_15k = []
            list_15k_20k = []
            list_20k_30k = []
            list_30k_40k = []
            list_40k_50k = []
            list_50k_60k = []
            list_60k_75k = []
            list_75k_100k = []
            list_100k_150k = []
            list_150k_200k = []
            list_over_200k = []
            
            #define lists definitions
            #main metrics
            list_umemployment_rate_def = []
            list_recent_job_growth_def = []
            list_future_job_growth_def = []
            list_sales_taxes_def = []
            list_income_tax_def = []
            list_income_per_capita_def = []
            list_household_income_def = []
            list_family_median_income_def = []
            #income distribution 

            list_under_15k_def = []
            list_15k_20k_def = []
            list_20k_30k_def = []
            list_30k_40k_def = []
            list_40k_50k_def = []
            list_50k_60k_def = []
            list_60k_75k_def = []
            list_75k_100k_def = []
            list_100k_150k_def = []
            list_150k_200k_def = []
            list_over_200k_def = []
                
            #pull html with selenium
            driver.get("https://www.bestplaces.net/economy/city/{}/{}".format(list_state_v2[i],list_city[i]))

            #pull economy data             
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[2]/td[2]"):
                    list_umemployment_rate.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_umemployment_rate.append(None)
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[3]/td[2]"):
                    list_recent_job_growth.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_recent_job_growth.append(None)
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[4/td[2]"):
                    list_future_job_growth.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_future_job_growth.append(None)
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[5]/td[2]"):
                    list_sales_taxes.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_sales_taxes.append(None)
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[6]/td[2]"):
                    list_income_tax.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_income_tax.append(None)
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[7]/td[2]"):
                    list_income_per_capita.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_income_per_capita.append(None)
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[8]/td[2]"):
                    list_household_income.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_household_income.append(None)
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[9]/td[2]"):
                    list_family_median_income.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                list_family_median_income.append(None)
            
            #income distribution
            try: 
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[3]/div/div/div[2]/script"):
                    list_income_distribution = element.get_attribute("innerHTML").split('data: ')[1].split(" }")[0].split(",")
                    list_under_15k.append(list_income_distribution[0].replace("[",''))         
                    list_15k_20k.append(list_income_distribution[1])       
                    list_20k_30k.append(list_income_distribution[2])       
                    list_30k_40k.append(list_income_distribution[3])       
                    list_40k_50k.append(list_income_distribution[4])       
                    list_50k_60k.append(list_income_distribution[5])       
                    list_60k_75k.append(list_income_distribution[6])       
                    list_75k_100k.append(list_income_distribution[7])       
                    list_100k_150k.append(list_income_distribution[8])       
                    list_150k_200k.append(list_income_distribution[9])       
                    list_over_200k.append(list_income_distribution[10].replace("]",''))  
           
            except:   
               list_under_15k.append(None)        
               list_15k_20k.append(None)       
               list_20k_30k.append(None)         
               list_30k_40k.append(None)        
               list_40k_50k.append(None)       
               list_50k_60k.append(None)          
               list_60k_75k.append(None)          
               list_75k_100k.append(None)      
               list_100k_150k.append(None)       
               list_150k_200k.append(None)         
               list_over_200k.append(None)                          
     
            
            if i == 0:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[2]/td[1]/button"):
                    list_umemployment_rate_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[3]/td[1]/button"):
                    list_recent_job_growth_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[4]/td[1]/button"):
                    list_future_job_growth_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[5]/td[1]/button"):
                    list_sales_taxes_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[6]/td[1]/button"):
                    list_income_tax_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[7]/td[1]/button"):
                    list_income_per_capita_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[8]/td[1]/button"):
                    list_household_income_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgEconomy']/tbody/tr[9]/td[1]/button"):
                    list_family_median_income_def.append(element.get_attribute('data-original-title'))

                list_under_15k_def.append("N/A")        
                list_15k_20k_def.append("N/A")       
                list_20k_30k_def.append("N/A")      
                list_30k_40k_def.append("N/A")       
                list_40k_50k_def.append("N/A")       
                list_50k_60k_def.append("N/A")        
                list_60k_75k_def.append("N/A")        
                list_75k_100k_def.append("N/A")         
                list_100k_150k_def.append("N/A")        
                list_150k_200k_def.append("N/A") 
                list_over_200k_def.append("N/A") 
                
            print('end economy data')
         
          
        #### PART 6 IMPORT PEOPLE DATA #### Source = bestplace.net 
        if var == True:
            
            
            print('start people data') 
            
            #define list data
            #people
            list_population = []
            list_female_population = []
            list_male_population = []
            list_median_age = []
            list_population_density = []
            list_land_area = []
            list_water_area = []
            #race
            list_white = []
            list_black = []
            list_asian = []
            list_native_american = []
            list_hawaiian_pacific_islander = []
            list_other_race = []
            list_two_or_more_races= []
            list_hispanic = []
            #marriage & family
            list_married_population = []
            list_currently_married = []
            list_married_but_seperated = []
            list_single_population = []
            list_never_married = []
            list_divorced = []
            list_widowed = []
            list_household_size = []
            list_households  = []
            list_family_households = []
            list_married_couple_with_children = []
            list_married_couple_without_children = []
            list_non_family_households = []
            list_single_householder_with_children = []
            list_single_householder_without_children = []
            #age breakdown 
            list_age_distribution = []
            list_0_4_years = []
            list_5_9_years = []
            list_10_14_years = []
            list_15_17_years = []
            list_18_20_years = []
            list_21_24_years = []
            list_25_34_years = []
            list_35_44_years = []
            list_45_54_years = []
            list_55_59_years = []
            list_60_64_years = []
            list_65_74_years = []
            list_75_84_years = []
            list_over_85_years = []
            
            #define list definitions
            #people
            list_population_def = []
            list_female_population_def = []
            list_male_population_def = []
            list_median_age_def = []
            list_population_density_def = []
            list_land_area_def = []
            list_water_area_def = []
            #race
            list_white_def = []
            list_black_def = []
            list_asian_def = []
            list_native_american_def = []
            list_hawaiian_pacific_islander_def = []
            list_other_race_def = []
            list_two_or_more_races_def = []
            list_hispanic_def = []
            #marriage & family
            list_married_population_def = []
            list_currently_married_def = []
            list_married_but_seperated_def = []
            list_single_population_def = []
            list_never_married_def = []
            list_divorced_def = []
            list_widowed_def = []
            list_household_size_def = []
            list_households_def  = []
            list_family_households_def = []
            list_married_couple_with_children_def = []
            list_married_couple_without_children_def = []
            list_non_family_households_def = []
            list_single_householder_with_children_def = []
            list_single_householder_without_children_def = []
            #age breakdown 
            list_0_4_years_def = []
            list_5_9_years_def = []
            list_10_14_years_def = []
            list_15_17_years_def = []
            list_18_20_years_def = []
            list_21_24_years_def = []
            list_25_34_years_def = []
            list_35_44_years_def = []
            list_45_54_years_def = []
            list_55_59_years_def = []
            list_60_64_years_def = []
            list_65_74_years_def = []
            list_75_84_years_def = []
            list_over_85_years_def = []
            
                 
            #pull html with selenium
            driver.get("https://www.bestplaces.net/people/city/{}/{}".format(list_state_v2[i],list_city[i]))
            
            #pull people data
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[2]/td[2]"):
                    list_population.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[3]/td[2]"):
                    list_female_population.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[4]/td[2]"):
                    list_male_population.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[5]/td[2]"):
                    list_median_age.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[14]/td[2]"):
                    list_population_density.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[15]/td[2]"):
                    list_land_area.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[16]/td[2]"):
                    list_water_area.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                    list_population.append(None)
                    list_female_population.append(None)
                    list_male_population.append(None)
                    list_median_age.append(None)
                    list_population_density.append(None)
                    list_land_area.append(None)
                    list_water_area.append(None)
                
            #pull race data
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[18]/td[2]"):
                    list_white.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[19]/td[2]"):
                    list_black.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[20]/td[2]"):
                    list_asian.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[21]/td[2]"):
                    list_native_american.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[22]/td[2]"):
                    list_hawaiian_pacific_islander.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[23]/td[2]"):
                    list_other_race.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[24]/td[2]"):
                    list_two_or_more_races.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[25]/td[2]"):
                    list_hispanic.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                    list_white.append(None)
                    list_black.append(None)
                    list_asian.append(None)
                    list_native_american.append(None)
                    list_hawaiian_pacific_islander.append(None)
                    list_two_or_more_races.append(None)
                    list_hispanic.append(None)
                
            #pull marriage & family data
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[27]/td[2]"):
                    list_married_population.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[28]/td[2]"):
                    list_currently_married.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[29]/td[2]"):
                    list_married_but_seperated.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[30]/td[2]"):
                    list_single_population.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[31]/td[2]"):
                    list_never_married.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[32]/td[2]"):
                    list_divorced.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[33]/td[2]"):
                    list_widowed.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[35]/td[2]"):
                    list_household_size.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[36]/td[2]"):
                    list_households.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[37]/td[2]"):
                    list_family_households.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[38]/td[2]"):
                    list_married_couple_with_children.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[39]/td[2]"):
                    list_married_couple_without_children.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[40]/td[2]"):
                    list_non_family_households.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[41]/td[2]"):
                    list_single_householder_with_children.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[42]/td[2]"):
                    list_single_householder_without_children.append(convert_str_to_float(element.get_attribute("innerText")))

            except:
                    list_married_population.append(None)
                    list_currently_married.append(None)
                    list_married_but_seperated.append(None)
                    list_single_population.append(None)
                    list_never_married.append(None)
                    list_divorced.append(None)
                    list_widowed.append(None)
                    list_household_size.append(None)
                    list_households.append(None)
                    list_family_households.append(None)
                    list_married_couple_with_children.append(None)
                    list_married_couple_without_children.append(None)
                    list_non_family_households.append(None)
                    list_single_householder_with_children.append(None)
                    list_single_householder_without_children.append(None)
                
            
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[3]/div/div/div[2]/script"):
                    list_age_distribution = element.get_attribute("innerHTML").split('data: ')[1].split(", ")[0].split(",")
                    list_0_4_years.append(list_age_distribution[0].replace("[",''))         
                    list_5_9_years.append(list_age_distribution[1])       
                    list_10_14_years.append(list_age_distribution[2])       
                    list_15_17_years.append(list_age_distribution[3])       
                    list_18_20_years.append(list_age_distribution[4])       
                    list_21_24_years.append(list_age_distribution[5])       
                    list_25_34_years.append(list_age_distribution[6])       
                    list_35_44_years.append(list_age_distribution[7])       
                    list_45_54_years.append(list_age_distribution[8])       
                    list_55_59_years.append(list_age_distribution[9])       
                    list_60_64_years.append(list_age_distribution[10])   
                    list_65_74_years.append(list_age_distribution[11])       
                    list_75_84_years.append(list_age_distribution[12])       
                    list_over_85_years.append(list_age_distribution[13].replace("]",''))    
          
            except:
                 list_0_4_years.append(None)      
                 list_5_9_years.append(None)      
                 list_10_14_years.append(None)        
                 list_15_17_years.append(None)          
                 list_18_20_years.append(None)     
                 list_21_24_years.append(None)         
                 list_25_34_years.append(None)       
                 list_35_44_years.append(None)         
                 list_45_54_years.append(None)      
                 list_55_59_years.append(None)          
                 list_60_64_years.append(None)     
                 list_65_74_years.append(None)         
                 list_75_84_years.append(None)        
                 list_over_85_years.append(None)    
               
                
            if i == 0:
                #pull people data
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[2]/td[1]/button"):
                    list_population_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[3]/td[1]/button"):
                    list_female_population_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[4]/td[1]/button"):
                    list_male_population_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[5]/td[1]/button"):
                    list_median_age_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[14]/td[1]/button"):
                    list_population_density_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[15]/td[1]/button"):
                    list_land_area_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[16]/td[1]/button"):
                    list_water_area_def.append(element.get_attribute('data-original-title'))
                    
                #pull race data
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[18]/td[1]/button"):
                    list_white_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[19]/td[1]/button"):
                    list_black_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[20]/td[1]/button"):
                    list_asian_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[21]/td[1]/button"):
                    list_native_american_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[22]/td[1]/button"):
                    list_hawaiian_pacific_islander_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[23]/td[1]/button"):
                    list_other_race_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[24]/td[1]/button"):
                    list_two_or_more_races_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[25]/td[1]/button"):
                    list_hispanic_def.append(element.get_attribute('data-original-title'))
                    
                #pull marriage & family data
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[27]/td[1]/button"):
                    list_married_population_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[28]/td[1]/button"):
                    list_currently_married_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[29]/td[1]/button"):
                    list_married_but_seperated_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[30]/td[1]/button"):
                    list_single_population_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[31]/td[1]/button"):
                    list_never_married_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[32]/td[1]/button"):
                    list_divorced_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[33]/td[1]/button"):
                    list_widowed_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[35]/td[1]/button"):
                    list_household_size_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[36]/td[1]/button"):
                    list_households_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[37]/td[1]/button"):
                    list_family_households_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[38]/td[1]/button"):
                    list_married_couple_with_children_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[39]/td[1]/button"):
                    list_married_couple_without_children_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[40]/td[1]/button"):
                    list_non_family_households_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[41]/td[1]/button"):
                    list_single_householder_with_children_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgPeople']/tbody/tr[42]/td[1]/button"):
                    list_single_householder_without_children_def.append(element.get_attribute('data-original-title'))
                    
            
                list_0_4_years_def.append("N/A")        
                list_5_9_years_def.append("N/A")       
                list_10_14_years_def.append("N/A")      
                list_15_17_years_def.append("N/A")     
                list_18_20_years_def.append("N/A")     
                list_21_24_years_def.append("N/A")     
                list_25_34_years_def.append("N/A")      
                list_35_44_years_def.append("N/A")     
                list_45_54_years_def.append("N/A")    
                list_55_59_years_def.append("N/A")      
                list_60_64_years_def.append("N/A") 
                list_65_74_years_def.append("N/A")     
                list_75_84_years_def.append("N/A")     
                list_over_85_years_def.append("N/A") 
                
            print('end people data')
            
        #### PART 7 IMPORT HEALTH DATA #### Source = bestplace.net 
        if var == True:
            
            print('start health data')
                
            #define lists data
            list_doctor_per_100k_pop = []
            list_cost_health_index = []
            list_water_index = []
            list_air_index = []
            
            #define lists definitions
            list_doctor_per_100k_pop_def = []
            list_cost_health_index_def = []
            list_water_index_def = []
            list_air_index_def = []
                            
            #pull html with selenium
            driver.get("https://www.bestplaces.net/health/city/{}/{}".format(list_state_v2[i],list_city[i]))
            
            #pull health data
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/p[1]"):
                    list_doctor_per_100k_pop.append(int(re.search(r'\d+', element.get_attribute("innerText")).group()))
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[3]"):
                    list_cost_health_index.append(convert_str_to_float(element.get_attribute("innerText").replace(" / 100", "")))
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[4]"):
                    list_water_index.append(convert_str_to_float(element.get_attribute("innerText").replace(" / 100", "")))
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[6]"):
                    list_air_index.append(convert_str_to_float(element.get_attribute("innerText").replace(" / 100", "")))
           
            except:      
                list_doctor_per_100k_pop.append(None)
                list_cost_health_index.append(None)
                list_water_index.append(None)
                list_air_index.append(None)
            
            #//*[@id="form1"]/div[7]/div[2]/div[2]/p[1]/text()
            if i ==0:
                list_doctor_per_100k_pop_def.append("N/A")
                list_cost_health_index_def.append("N/A")
                list_water_index_def.append("N/A")
                list_air_index_def.append("N/A")
              
                
            print('end health data')
        
        #### PART 8 IMPORT POLITICS DATA #### Source = bestplace.net 
        if var == True:
            
            print('start politics data')
            
            #define lists data
            list_previous_presidential_elections = []
            list_previous_presidential_election_democrats = []
            list_previous_presidential_election_republicans = []
            list_previous_presidential_election_independants = []
            list_count_contributions_democrats = []
            list_sum_contributions_democrats = []
            list_count_contributions_republicans = []
            list_sum_contributions_republicans = []
            #list_seats_democrats = []
            #list_seats_republicans = []
            #list_seats_independents = []
            
            #define lists definitions
            list_previous_presidential_elections_def = []
            list_previous_presidential_election_democrats_def = []
            list_previous_presidential_election_republicans_def = []
            list_previous_presidential_election_independants_def = []
            list_count_contributions_democrats_def = []
            list_sum_contributions_democrats_def = []
            list_count_contributions_republicans_def = []
            list_sum_contributions_republicans_def = []
            
            #pull html with selenium
            driver.get("https://www.bestplaces.net/voting/city/{}/{}".format(list_state_v2[i],list_city[i]))

            #pull politics data
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/h5[3]"):
                    list_previous_presidential_elections.append(element.get_attribute("innerText").replace(list_city[i],'').replace(list_state_v2[i],"").replace(", : ",""))
            except:
                list_previous_presidential_elections.append("N/A")
                
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p[2]/b[1]"):
                    list_previous_presidential_election_democrats.append(re.findall(r"[-+]?\d*\.\d+|\d+", element.get_attribute("innerText"))[0])
            except:
                list_previous_presidential_election_democrats.append("N/A")                  

            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p[2]/b[2]"):
                    list_previous_presidential_election_republicans.append(re.findall(r"[-+]?\d*\.\d+|\d+", element.get_attribute("innerText"))[0])
            except:
                list_previous_presidential_election_republicans.append("N/A")

            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p[2]/b[3]"):
                    list_previous_presidential_election_independants.append(re.findall(r"[-+]?\d*\.\d+|\d+", element.get_attribute("innerText"))[0])
            except:
                list_previous_presidential_election_independants.append("N/A")
            
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p[8]"):
                    list_count_contributions_democrats.append(list(re.findall(r"[-+]?\d*\.\d+|\d+", element.get_attribute("innerText").split('totaling')[0].split('there were')[1].replace(",","")))[0])
            except:
                list_count_contributions_democrats.append("N/A")

            try:   
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p[8]"):
                    list_sum_contributions_democrats.append(list(re.findall(r"[-+]?\d*\.\d+|\d+", element.get_attribute("innerText").split('totaling')[1].replace(",","")))[0])
            except:
                list_sum_contributions_democrats.append("N/A")
             
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p[9]"):
                    list_count_contributions_republicans.append(list(re.findall(r"[-+]?\d*\.\d+|\d+", element.get_attribute("innerText").split('totaling')[0].split('there were')[1].replace(",","")))[0])
            except:
                list_count_contributions_republicans.append("N/A")
                
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p[9]"):
                    list_sum_contributions_republicans.append(list(re.findall(r"[-+]?\d*\.\d+|\d+", element.get_attribute("innerText").split('totaling')[1].split("campaigns")[0].replace(",","")))[0])
            except:
                list_sum_contributions_republicans.append("N/A")
            
            #for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[3]/div/div/div[2]/script"):
                #list_seats_democrats.append(element.get_attribute("innerHTML").split('data: ')[1].split(", ")[0].split(",")[1])  
                #list_seats_republicans.append(element.get_attribute("innerHTML").split('data: ')[1].split(", ")[1].split(",")[1])    
                #list_seats_independents.append(element.get_attribute("innerHTML").split('data: ')[1].split(", ")[2].split(",")[1])     

            #pull definitions
            if i == 0:
                try:
                    for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p[6]"):
                        list_previous_presidential_elections_def.append(element.get_attribute("innerText"))
                except:
                    list_previous_presidential_elections_def.append("N/A")
                list_previous_presidential_election_democrats_def.append("N/A")
                list_previous_presidential_election_republicans_def.append("N/A")
                list_previous_presidential_election_independants_def.append("N/A")
                list_count_contributions_democrats_def.append("N/A")
                list_sum_contributions_democrats_def.append("N/A")
                list_count_contributions_republicans_def.append("N/A")
                list_sum_contributions_republicans_def.append("N/A")
                
        
            print('end politics data')
            
        #### PART 9 IMPORT RELIGION DATA #### Source = bestplace.net 
        if var == True:
            
            print('start religion data')
            
            #define lists data
            list_religious = []
            list_baptist = []
            list_episcopalian = []
            list_catholic = []
            list_lutheran = []
            list_methodist = []
            list_pentecostal = []
            list_presbyterian = []
            list_jesus_christ = []
            list_christian_faith = []
            list_jusdaism = []
            list_eastern_faith = []
            list_islam = []
            
            #define lists data
            list_religious_def = []
            list_baptist_def = []
            list_episcopalian_def = []
            list_catholic_def = []
            list_lutheran_def = []
            list_methodist_def = []
            list_pentecostal_def = []
            list_presbyterian_def = []
            list_jesus_christ_def = []
            list_christian_faith_def = []
            list_jusdaism_def = []
            list_eastern_faith_def = []
            list_islam_def = []
            
            #pull html with selenium
            driver.get("https://www.bestplaces.net/religion/city/{}/{}".format(list_state_v2[i],list_city[i]))
        
            #pull religion data
            try: 
                for element in driver.find_elements(By.XPATH, "//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p"):
                    list_temp = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", element.get_attribute("innerText"))))
                    list_religious.append(list_temp[0])
                    list_baptist.append(list_temp[1])
                    list_episcopalian.append(list_temp[2])
                    list_catholic.append(list_temp[3])
                    list_lutheran.append(list_temp[4])
                    list_methodist.append(list_temp[5])
                    list_pentecostal.append(list_temp[6])
                    list_presbyterian.append(list_temp[7])
                    list_jesus_christ.append(list_temp[8])
                    list_christian_faith.append(list_temp[9])
                    list_jusdaism.append(list_temp[10])
                    list_eastern_faith.append(list_temp[11])
                    list_islam.append(list_temp[12])
            except:
                 list_religious.append(None)
                 list_baptist.append(None)
                 list_episcopalian.append(None)
                 list_catholic.append(None)
                 list_lutheran.append(None)
                 list_methodist.append(None)
                 list_pentecostal.append(None)
                 list_presbyterian.append(None)
                 list_jesus_christ.append(None)
                 list_christian_faith.append(None)
                 list_jusdaism.append(None)
                 list_eastern_faith.append(None)
                 list_islam.append(None)
                
            
            if i ==0:
                list_religious_def.append("N/A")
                list_baptist_def.append("N/A")
                list_episcopalian_def.append("N/A")
                list_catholic_def.append("N/A")
                list_lutheran_def.append("N/A")
                list_methodist_def.append("N/A")
                list_pentecostal_def.append("N/A")
                list_presbyterian_def.append("N/A")
                list_jesus_christ_def.append("N/A")
                list_christian_faith_def.append("N/A")
                list_jusdaism_def.append("N/A")
                list_eastern_faith_def.append("N/A")
                list_islam_def.append("N/A")
                
            print('end religion data')
            
        #### PART 10 IMPORT HOUSING DATA #### Source = bestplace.net 
        if var == True:
            
            print('start housing data')
            
            #define lists data
            #housing
            list_number_homes = []
            list_median_home_age = []
            list_median_home_cost = []
            list_home_appreciation_last_12_months = []
            list_home_appreciation_last_5_months = []
            list_home_appreciation_last_10_months = []
            list_property_tax_rates = []
            list_property_tax_paid = []
            list_homes_owned = []
            list_housing_vacant = []
            list_homes_rented = [] 
            #vacant housing
            list_vacant_for_rent = []
            list_vacant_rented = []   
            list_vacant_for_sale = []
            list_vacant_sold = []
            list_vacant_vacation = []
            list_vacant_other = []
            #value of owner-occupied housing
            list_own_occupied_houses_less_than_20k = []
            list_own_occupied_houses_between_20k_and_40k = []
            list_own_occupied_houses_between_40k_and_60k = []
            list_own_occupied_houses_between_60k_and_80k = []   
            list_own_occupied_houses_between_80k_and_100k = []   
            list_own_occupied_houses_between_100k_and_150k = []   
            list_own_occupied_houses_between_150k_and_200k = [] 
            list_own_occupied_houses_between_200k_and_300k = [] 
            list_own_occupied_houses_between_300k_and_400k = []    
            list_own_occupied_houses_between_400k_and_500k = [] 
            list_own_occupied_houses_between_500k_and_750k = [] 
            list_own_occupied_houses_between_750k_and_1000k = [] 
            list_own_occupied_houses_between_1000k_and_1500k = [] 
            list_own_occupied_houses_between_1500k_and_2000k = []
            list_own_occupied_houses_more_than_2000k = [] 
            #housing units by year structured
            list_housing_units_younger_than_2014 = []
            list_housing_units_between_2010_and_2013 = []
            list_housing_units_between_2000_and_2009 = []
            list_housing_units_between_1990_and_1999 = []
            list_housing_units_between_1980_and_1989 = []
            list_housing_units_between_1970_and_1979 = []
            list_housing_units_between_1960_and_1969 = []
            list_housing_units_between_1950_and_1959 = []
            list_housing_units_between_1940_and_1949 = []
            list_housing_units_older_than_1939 = []
            
            #pull lists definitions
            #housing
            list_number_homes_def = []
            list_median_home_age_def = []
            list_median_home_cost_def = []
            list_home_appreciation_last_12_months_def = []
            list_home_appreciation_last_5_months_def = []
            list_home_appreciation_last_10_months_def = []
            list_property_tax_rates_def = []
            list_property_tax_paid_def = []
            list_homes_owned_def = []
            list_housing_vacant_def = []
            list_homes_rented_def = [] 
            #vacant housing
            list_vacant_for_rent_def = []
            list_vacant_rented_def = []   
            list_vacant_for_sale_def = []
            list_vacant_sold_def = []
            list_vacant_vacation_def = []
            list_vacant_other_def = []
            #value of owner-occupied housing
            list_own_occupied_houses_less_than_20k_def = []
            list_own_occupied_houses_between_20k_and_40k_def = []
            list_own_occupied_houses_between_40k_and_60k_def = []
            list_own_occupied_houses_between_60k_and_80k_def = []   
            list_own_occupied_houses_between_80k_and_100k_def = []   
            list_own_occupied_houses_between_100k_and_150k_def = []   
            list_own_occupied_houses_between_150k_and_200k_def = [] 
            list_own_occupied_houses_between_200k_and_300k_def = [] 
            list_own_occupied_houses_between_300k_and_400k_def = []    
            list_own_occupied_houses_between_400k_and_500k_def = [] 
            list_own_occupied_houses_between_500k_and_750k_def = [] 
            list_own_occupied_houses_between_750k_and_1000k_def = [] 
            list_own_occupied_houses_between_1000k_and_1500k_def = [] 
            list_own_occupied_houses_between_1500k_and_2000k_def = []
            list_own_occupied_houses_more_than_2000k_def = [] 
            #housing units by year structured
            list_housing_units_younger_than_2014_def = []
            list_housing_units_between_2010_and_2013_def = []
            list_housing_units_between_2000_and_2009_def = []
            list_housing_units_between_1990_and_1999_def = []
            list_housing_units_between_1980_and_1989_def = []
            list_housing_units_between_1970_and_1979_def = []
            list_housing_units_between_1960_and_1969_def = []
            list_housing_units_between_1950_and_1959_def = []
            list_housing_units_between_1940_and_1949_def = []
            list_housing_units_older_than_1939_def = []
            
               
            #pull html with selenium
            driver.get("https://www.bestplaces.net/housing/city/{}/{}".format(list_state_v2[i],list_city[i]))
            
            #pull housing data
            #housing
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[2]/td[2]"):
                    list_number_homes.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[3]/td[2]"):
                    list_median_home_age.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[4]/td[2]"):
                    list_median_home_cost.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[5]/td[2]"):
                    list_home_appreciation_last_12_months.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[6]/td[2]"):
                    list_home_appreciation_last_5_months.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[7]/td[2]"):
                    list_home_appreciation_last_10_months.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[8]/td[2]"):
                    list_property_tax_rates.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[9]/td[2]"):
                    list_property_tax_paid.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[10]/td[2]"):
                    list_homes_owned.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[11]/td[2]"):
                    list_housing_vacant.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[12]/td[2]"):
                    list_homes_rented.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                    list_number_homes.append(None)
                    list_median_home_age.append(None)
                    list_median_home_cost.append(None)
                    list_home_appreciation_last_12_months.append(None)
                    list_home_appreciation_last_5_months.append(None)
                    list_home_appreciation_last_10_months.append(None)
                    list_property_tax_rates.append(None)
                    list_property_tax_paid.append(None)
                    list_homes_owned.append(None)
                    list_housing_vacant.append(None)
                    list_homes_rented.append(None)
            
            #vacant housing
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[14]/td[2]"):
                    list_vacant_for_rent.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[15]/td[2]"):
                    list_vacant_rented.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[16]/td[2]"):
                    list_vacant_for_sale.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[17]/td[2]"):
                    list_vacant_sold.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[18]/td[2]"):
                    list_vacant_vacation.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[19]/td[2]"):
                    list_vacant_other.append(convert_str_to_float(element.get_attribute("innerText")))
            except:
                    list_vacant_for_rent.append(None)
                    list_vacant_rented.append(None)
                    list_vacant_for_sale.append(None)
                    list_vacant_sold.append(None)
                    list_vacant_vacation.append(None)
                    list_vacant_other.append(None)
             
        
            #value of owner-occupied housing
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[21]/td[2]"):
                    list_own_occupied_houses_less_than_20k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[22]/td[2]"):
                    list_own_occupied_houses_between_20k_and_40k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[23]/td[2]"):
                    list_own_occupied_houses_between_40k_and_60k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[24]/td[2]"):
                    list_own_occupied_houses_between_60k_and_80k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[25]/td[2]"):
                    list_own_occupied_houses_between_80k_and_100k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[26]/td[2]"):
                    list_own_occupied_houses_between_100k_and_150k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[27]/td[2]"):
                    list_own_occupied_houses_between_150k_and_200k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[28]/td[2]"):
                    list_own_occupied_houses_between_200k_and_300k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[29]/td[2]"):
                    list_own_occupied_houses_between_300k_and_400k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[30]/td[2]"):
                    list_own_occupied_houses_between_400k_and_500k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[31]/td[2]"):
                    list_own_occupied_houses_between_500k_and_750k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[32]/td[2]"):
                    list_own_occupied_houses_between_750k_and_1000k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[33]/td[2]"):
                    list_own_occupied_houses_between_1000k_and_1500k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[34]/td[2]"):
                    list_own_occupied_houses_between_1500k_and_2000k.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[35]/td[2]"):
                    list_own_occupied_houses_more_than_2000k.append(convert_str_to_float(element.get_attribute("innerText")))
            
            except:
                    list_own_occupied_houses_less_than_20k.append(None)
                    list_own_occupied_houses_between_20k_and_40k.append(None)
                    list_own_occupied_houses_between_40k_and_60k.append(None)
                    list_own_occupied_houses_between_60k_and_80k.append(None)
                    list_own_occupied_houses_between_80k_and_100k.append(None)
                    list_own_occupied_houses_between_100k_and_150k.append(None)
                    list_own_occupied_houses_between_150k_and_200k.append(None)
                    list_own_occupied_houses_between_200k_and_300k.append(None)
                    list_own_occupied_houses_between_300k_and_400k.append(None)
                    list_own_occupied_houses_between_400k_and_500k.append(None)
                    list_own_occupied_houses_between_500k_and_750k.append(None)
                    list_own_occupied_houses_between_750k_and_1000k.append(None)
                    list_own_occupied_houses_between_1000k_and_1500k.append(None)
                    list_own_occupied_houses_between_1500k_and_2000k.append(None)
                    
                    
            #housing units by year structured
            try:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[37]/td[2]"):
                    list_housing_units_younger_than_2014.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[38]/td[2]"):
                    list_housing_units_between_2010_and_2013.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[39]/td[2]"):
                    list_housing_units_between_2000_and_2009.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[40]/td[2]"):
                    list_housing_units_between_1990_and_1999.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[41]/td[2]"):
                    list_housing_units_between_1980_and_1989.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[42]/td[2]"):
                    list_housing_units_between_1970_and_1979.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[43]/td[2]"):
                    list_housing_units_between_1960_and_1969.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[44]/td[2]"):
                    list_housing_units_between_1950_and_1959.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[45]/td[2]"):
                    list_housing_units_between_1940_and_1949.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[46]/td[2]"):
                    list_housing_units_older_than_1939.append(convert_str_to_float(element.get_attribute("innerText")))
                
            except:
                    list_housing_units_younger_than_2014.append(None)
                    list_housing_units_between_2010_and_2013.append(None)
                    list_housing_units_between_2000_and_2009.append(None)
                    list_housing_units_between_1990_and_1999.append(None)
                    list_housing_units_between_1980_and_1989.append(None)
                    list_housing_units_between_1970_and_1979.append(None)
                    list_housing_units_between_1960_and_1969.append(None)
                    list_housing_units_between_1950_and_1959.append(None)
                    list_housing_units_between_1940_and_1949.append(None)
                    list_housing_units_older_than_1939.append(None)
    
            
            #pull definitions
            if i == 0:
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[2]/td[1]/button"):
                    list_number_homes_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[3]/td[1]/button"):
                    list_median_home_age_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[4]/td[1]/button"):
                    list_median_home_cost_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[5]/td[1]/button"):
                    list_home_appreciation_last_12_months_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[6]/td[1]/button"):
                    list_home_appreciation_last_5_months_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[7]/td[1]/button"):
                    list_home_appreciation_last_10_months_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[8]/td[1]/button"):
                    list_property_tax_rates_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[9]/td[1]/button"):
                    list_property_tax_paid_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[10]/td[1]/button"):
                    list_homes_owned_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[11]/td[1]/button"):
                    list_housing_vacant_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[12]/td[1]/button"):
                    list_homes_rented_def.append(element.get_attribute('data-original-title'))
                    
                #vacant housing
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[14]/td[1]/button"):
                    list_vacant_for_rent_def.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[15]/td[1]/button"):
                    list_vacant_rented_def.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[16]/td[1]/button"):
                    list_vacant_for_sale_def.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[17]/td[1]/button"):
                    list_vacant_sold_def.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[18]/td[1]/button"):
                    list_vacant_vacation_def.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[19]/td[1]/button"):
                    list_vacant_other_def.append(convert_str_to_float(element.get_attribute("innerText")))
            
                #value of owner-occupied housing
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[21]/td[1]/button"):
                    list_own_occupied_houses_less_than_20k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[22]/td[1]/button"):
                    list_own_occupied_houses_between_20k_and_40k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[23]/td[1]/button"):
                    list_own_occupied_houses_between_40k_and_60k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[24]/td[1]/button"):
                    list_own_occupied_houses_between_60k_and_80k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[25]/td[1]/button"):
                    list_own_occupied_houses_between_80k_and_100k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[26]/td[1]/button"):
                    list_own_occupied_houses_between_100k_and_150k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[27]/td[1]/button"):
                    list_own_occupied_houses_between_150k_and_200k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[28]/td[1]/button"):
                    list_own_occupied_houses_between_200k_and_300k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[29]/td[1]/button"):
                    list_own_occupied_houses_between_300k_and_400k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[30]/td[1]/button"):
                    list_own_occupied_houses_between_400k_and_500k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[31]/td[1]/button"):
                    list_own_occupied_houses_between_500k_and_750k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[32]/td[1]/button"):
                    list_own_occupied_houses_between_750k_and_1000k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[33]/td[1]/button"):
                    list_own_occupied_houses_between_1000k_and_1500k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[34]/td[1]/button"):
                    list_own_occupied_houses_between_1500k_and_2000k_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[35]/td[1]/button"):
                    list_own_occupied_houses_more_than_2000k_def.append(element.get_attribute('data-original-title'))
            
                #housing units by year structured
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[37]/td[1]/button"):
                    list_housing_units_younger_than_2014_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[38]/td[1]/button"):
                    list_housing_units_between_2010_and_2013_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[39]/td[1]/button"):
                    list_housing_units_between_2000_and_2009_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[40]/td[1]/button"):
                    list_housing_units_between_1990_and_1999_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[41]/td[1]/button"):
                    list_housing_units_between_1980_and_1989_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[42]/td[1]/button"):
                    list_housing_units_between_1970_and_1979_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[43]/td[1]/button"):
                    list_housing_units_between_1960_and_1969_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[44]/td[1]/button"):
                    list_housing_units_between_1950_and_1959_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[45]/td[1]/button"):
                    list_housing_units_between_1940_and_1949_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgHousing']/tbody/tr[46]/td[1]/button"):
                    list_housing_units_older_than_1939_def.append(element.get_attribute('data-original-title'))

                
            #print('end housing data')
        
        #### PART 11 IMPORT COMMUTE DATA #### Source = bestplace.net 
        if var == True:
        
            #print('start commute data')
            
            #define lists data
            #commute time
            list_commute_time = []
            #commute mode
            list_commute_auto_alone = []
            list_commute_carpool = []
            list_commute_mass_transit = []
            list_commute_bicycle = []
            list_commute_walk = []
          
            #define lists definitions
            #commute time
            list_commute_time_def = []
            #commute mode
            list_commute_auto_alone_def = []
            list_commute_carpool_def = []
            list_commute_mass_transit_def = []
            list_commute_bicycle_def = []
            list_commute_walk_def = []
        
               
            #pull html with selenium
            driver.get("https://www.bestplaces.net/transportation/city/{}/{}".format(list_state_v2[i],list_city[i]))
            
            #pull data
            try:
                #pull commute time data
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[2]/td[2]"):
                    list_commute_time.append(convert_str_to_float(element.get_attribute("innerText")))
                #pull commute mode data
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[4]/td[2]"):
                    list_commute_auto_alone.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[5]/td[2]"):
                    list_commute_carpool.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[6]/td[2]"):
                    list_commute_mass_transit.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[7]/td[2]"):
                    list_commute_bicycle.append(convert_str_to_float(element.get_attribute("innerText")))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[8]/td[2]"):
                    list_commute_walk.append(convert_str_to_float(element.get_attribute("innerText")))
        
            except:
                   list_commute_time.append(None)
                   list_commute_auto_alone.append(None)
                   list_commute_carpool.append(None)
                   list_commute_mass_transit.append(None)
                   list_commute_bicycle.append(None)
                   list_commute_walk.append(None)
        
            if i == 0:       
                #pull definitions
                #pull commute time data
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[2]/td[1]/button"):
                    list_commute_time_def.append(element.get_attribute('data-original-title'))
                #pull commute mode data
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[4]/td[1]/button"):
                    list_commute_auto_alone_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[5]/td[1]/button"):
                    list_commute_carpool_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[6]/td[1]/button"):
                    list_commute_mass_transit_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[7]/td[1]/button"):
                    list_commute_bicycle_def.append(element.get_attribute('data-original-title'))
                for element in driver.find_elements(By.XPATH, "//*[@id='mainContent_dgTransportation']/tbody/tr[8]/td[1]/button"):
                    list_commute_walk_def.append(element.get_attribute('data-original-title'))
        
            print('end commute data')
        
        #### PART 12 EXPORT  DATA #### Source = bestplace.net 
        if var == True:
            
            #export main data to dataframe
            data = {"City" : list_city, "State" : list_state, 'Average_Precipitation' : list_rainfall, 'Average_Snowfall' : list_snowfall,'Average_Rainy_Days' : list_average_rainy_days, 'Average_Sunny_Days': list_average_sunny_days,'Average_High_Jul' : list_average_high_jul, 'Average_Low_Jan' : list_average_low_jan, 'Comfort_Index' : list_comfort_index, 'UV_Index' : list_uv_index, 'Elevation' : list_elevation, "Land_Area" : list_land_area, "Water_Area" : list_water_area, "Cost_Living_Overall" : list_cost_of_living_overall, "Cost_Grocery" : list_cost_of_grocery, "Cost_Health" : list_cost_of_health, "Cost_Housing" : list_cost_of_housing, "Cost_Median_Home" : list_cost_of_median_home_cost, "Cost_Utilites" : list_cost_of_utilities, "Cost_Transportation" : list_cost_of_transportation, "Cost_Miscellaneous" : list_cost_of_miscellanous, "Count_Violent_Crimes" : list_violent, "Count_Murders" : list_murder, "Count_Rapes" : list_rape, "Count_Robberies" : list_robbery, "Count_Assaults" : list_assault, "Count_Property_Crimes" : list_property, "Count_Bulgaries" : list_bulgary, "Count_Larcenies" : list_larceny, "Count_Autos" : list_auto, "Index_Violent_Crimes" : list_index_violent, "Index_Property_Crimes" : list_index_property, "Overall_Expenses_Per_Student" : list_overall_expenses_per_student, "Education_Expenses_Per_Student" : list_education_expenses_per_student, "Instruction_Expenses_Per_Student" : list_instruction_expenses_per_student, "Count_Students_Per_Teacher" : list_student_per_teacher, "Count_Students_Per_Librarian" : list_students_per_librarian, "Count_Students_Per_Counselor" : list_students_per_counselor, "Percentage_Grade_School" : list_grade_school, "Percentage_Some_High_School" : list_some_high_school, "Percentage_High_School_Grad" : list_high_school_grad, "Percentage_High_School_Grad_Only" : list_high_school_grad_only, "Percentage_Some_College" : list_some_college, "Percentage_Degree_Two_Years" : list_degree_two_years, "Percentage_Degree_Four_Years" : list_degree_four_years, "Percentage_Degree_Four_Years_Only" : list_degree_four_year_only, "Percentage_Degree_Master" : list_degree_masters, "Percentage_Degree_Professional" : list_degree_professional, "Unemployment_Rate" : list_umemployment_rate, "Recent_Job_Growth" : list_recent_job_growth, "Future_Job_Growth" : list_future_job_growth, "Sales_Taxes" : list_sales_taxes, "Income_Tax" : list_income_tax, "Income_Per_Capita" : list_income_per_capita, "Household_Income" : list_household_income, "Family_Median_Income" : list_family_median_income, "Percentage_Income_Under_15k" : list_under_15k, "Percentage_Income_15k_20k" : list_15k_20k, "Percentage_Income_20k_30k" : list_20k_30k, "Percentage_Income_30k_40k" : list_30k_40k, "Percentage_Income_40k_50k" : list_40k_50k, "Percentage_Income_50k_60k" : list_50k_60k, "Percentage_Income_60k_75k" : list_60k_75k, "Percentage_Income_75k_100k" : list_75k_100k, "Percentage_Income_100k_150k" : list_100k_150k,  "Percentage_Income_150k_200k" : list_150k_200k, "Percentage_Income_over_200k" : list_over_200k,  "Population" : list_population, "Percentage_Female_Population" : list_female_population, "Percentage_Male_Population" : list_male_population, "Median_Age" : list_median_age, "Density_Population" : list_population_density, "Percentage_White_Population" : list_white, "Percentage_Black_Population" : list_black, "Percentage_Asian_Population" : list_asian, "Percentage_Native_American_Population" : list_native_american, "Percentage_Hawaiian_Pacific_Islander_Population" : list_hawaiian_pacific_islander, "Percentage_Other_Race_Population" : list_other_race, "Percentage_Two_Or_More_Races_Population" : list_two_or_more_races, "Percentage_Hispanic_Population" : list_hispanic, "Percentage_Married_Population" : list_married_population, "Percentage_Currently_Married_Population" : list_currently_married, "Percentage_Married_But_Seperated_Population" : list_married_but_seperated, "Percentage_Single_Population" : list_single_population, "Percentage_Never_Married_Population" : list_never_married, "Percentage_Divorced_Population" : list_divorced, "Percentage_Widowed_Population" : list_widowed, "Household_Size" : list_household_size, "Count_Households" : list_households, "Count_Family_Households" : list_family_households, "Percentage_Married_Couples_With_Children" : list_married_couple_with_children, "Percentage_Married_Couples_Without_Children" : list_married_couple_without_children, "Count_Non_Family_Households" : list_non_family_households, "Percentage_Single_Householder_With_Children" : list_single_householder_with_children, "Percentage_Single_Householder_Without_Children" : list_single_householder_without_children, "Percentage_0_4_years" : list_0_4_years,"Percentage_5_9_years" : list_5_9_years, "Percentage_10_14_years" : list_10_14_years, "Percentage_15_17_years" : list_15_17_years, "Percentage_18_20_years" : list_18_20_years, "Percentage_21_24_years" : list_21_24_years, "Percentage_25_34_years" : list_25_34_years, "Percentage_35_44_years" : list_35_44_years, "Percentage_45_54_years" : list_45_54_years, "Percentage_55_59_years" : list_55_59_years, "Percentage_60_64_years" : list_60_64_years, "Percentage_65_74_years" : list_65_74_years, "Percentage_75_84_years" : list_75_84_years, "Percentage_over_85_years" : list_over_85_years, "Count_Doctors_Per_100k_Pop" : list_doctor_per_100k_pop, "Cost_Health_Index" : list_cost_health_index, "Water_Index" : list_water_index, "Air_Index" : list_air_index, "Results_Previous_Presidential_Elections" : list_previous_presidential_elections, "Percentage_Democrats_Previous_Presidential_Election" :  list_previous_presidential_election_democrats, "Percentage_Republicans_Previous_Presidential_Election" : list_previous_presidential_election_republicans, "Percentage_Independents_Previous_Presidential_Election" : list_previous_presidential_election_independants, "Count_Contributions_Democrats" : list_count_contributions_democrats, "Sum_Contributions_Democrats" : list_sum_contributions_democrats, "Count_Contributions_Republicans" : list_count_contributions_republicans,"Sum_Contributions_Republicans" : list_sum_contributions_republicans, "Percentage_Religous" : list_religious, "Percentage_Baptist" : list_baptist, "Percentage_Episcopalian" : list_episcopalian, "Percentage_Catholic" : list_catholic , "Percentage_Lutheran" : list_lutheran, "Percentage_Methodologist" : list_methodist, "Percentage_Pentecostal" : list_pentecostal, "Percentage_Prebysterian" : list_pentecostal, "Percentage_Jesus_Christ" : list_jesus_christ, "Percentage_Christian" : list_christian_faith, "Percentage_Judaism" : list_jusdaism, "Percentage_Eastern_Faith" : list_eastern_faith, "Percentage_Islam" : list_islam, "Count_Number_Homes" :  list_number_homes, "Median_Home_Age" : list_median_home_age, "Median_Home_Cost" : list_median_home_cost, "Home_Appreciation_12_months" : list_home_appreciation_last_12_months, "Home_Appreciation_5_years" : list_home_appreciation_last_5_months, "Home_Appreciation_10_years" : list_home_appreciation_last_10_months, "Property_Tax_Rates" : list_property_tax_rates, "Average_Property_Tax_Paid" : list_property_tax_paid, "Percentage_Homes_Owned" : list_homes_owned, "Percentage_Homes_Vacant" : list_housing_vacant, "Percentage_Homes_Rented" : list_homes_rented, "Percentage_Vacant_For_Rent" : list_vacant_for_rent,  "Percentage_Vacant_Rented" :  list_vacant_rented, "Percentage_Vacant_For_Sale" : list_vacant_for_sale, "Percentage_Vacant_Sold" : list_vacant_sold, "Percentage_Vacant_For_Vacation" : list_vacant_vacation, "Percentage_Vacant_Other" : list_vacant_other,  "Percentage_Own_Occupied_House_Less_20K" : list_own_occupied_houses_less_than_20k, "Percentage_Own_Occupied_House_Between_20K_And_40K" :  list_own_occupied_houses_between_20k_and_40k, "Percentage_Own_Occupied_House_Between_40K_And_60K" :  list_own_occupied_houses_between_40k_and_60k, "Percentage_Own_Occupied_House_Between_60K_And_80K" :  list_own_occupied_houses_between_60k_and_80k, "Percentage_Own_Occupied_House_Between_80K_And_100K" :  list_own_occupied_houses_between_80k_and_100k, "Percentage_Own_Occupied_House_Between_100K_And_150K" :  list_own_occupied_houses_between_100k_and_150k, "Percentage_Own_Occupied_House_Between_150K_And_200K" :  list_own_occupied_houses_between_150k_and_200k, "Percentage_Own_Occupied_House_Between_200K_And_300K" :  list_own_occupied_houses_between_200k_and_300k, "Percentage_Own_Occupied_House_Between_300K_And_400K" :  list_own_occupied_houses_between_300k_and_400k, "Percentage_Own_Occupied_House_Between_400K_And_500K" :  list_own_occupied_houses_between_400k_and_500k, "Percentage_Own_Occupied_House_Between_500K_And_750K" :  list_own_occupied_houses_between_500k_and_750k, "Percentage_Own_Occupied_House_Between_750K_And_1000K" :  list_own_occupied_houses_between_750k_and_1000k, "Percentage_Own_Occupied_House_Between_1000K_And_1500K" :  list_own_occupied_houses_between_1000k_and_1500k, "Percentage_Own_Occupied_House_Between_1500K_And_2000K" :  list_own_occupied_houses_between_1500k_and_2000k, "Percentage_Own_Occupied_House_More_2000K" :  list_own_occupied_houses_more_than_2000k, "Percentage_Houses_Younger_2014" : list_housing_units_younger_than_2014,  "Percentage_Houses_Between_2010_And_2013" : list_housing_units_between_2010_and_2013, "Percentage_Houses_Between_2000_And_2009" : list_housing_units_between_2000_and_2009, "Percentage_Houses_Between_1990_And_1999" : list_housing_units_between_1990_and_1999, "Percentage_Houses_Between_1980_And_1989" : list_housing_units_between_1980_and_1989, "Percentage_Houses_Between_1970_And_1979" : list_housing_units_between_1970_and_1979, "Percentage_Houses_Between_1960_And_1969" : list_housing_units_between_1960_and_1969, "Percentage_Houses_Between_1950_And_1959" : list_housing_units_between_1950_and_1959, "Percentage_Houses_Between_1940_And_1949" : list_housing_units_between_1940_and_1949, "Percentage_Houses_Older_1949" : list_housing_units_older_than_1939, "Commute_Time_Minute" : list_commute_time, "Percentage_Commute_Auto_Alone" : list_commute_auto_alone, "Percentage_Commute_Carpool" : list_commute_carpool, "Percentage_Commute_Mass_Transit" :  list_commute_mass_transit, "Percentage_Commute_Bicycle" : list_commute_bicycle, "Percentage_Commute_Walk" : list_commute_walk}      
            df_temp = pd.DataFrame(data)
            
            #export list of city to dataframe
            #data_city = {"City" : list_city, "State" : list_state}
            #df_city = pd.DataFrame(data_city)                
            
            #export column names data to dataframe
            #data_column = {"Column" : df_temp.columns}
            #df_column = pd.DataFrame(data_column) 
            
            #export new data to dataframe
            #data_new_col = {"City" : list_city[i], "State" : list_state[i], "Percentage_Grade_School" : list_grade_school, "Percentage_Some_High_School" : list_some_high_school, "Percentage_High_School_Grad" : list_high_school_grad, "Percentage_High_School_Grad_Only" : list_high_school_grad_only, "Percentage_Some_College" : list_some_college, "Percentage_Degree_Two_Years" : list_degree_two_years, "Percentage_Degree_Four_Years" : list_degree_four_years, "Percentage_Degree_Four_Years_Only" : list_degree_four_year_only, "Percentage_Degree_Master" : list_degree_masters, "Percentage_Degree_Professional" : list_degree_professional, "Percentage_Income_Under_15k" : list_under_15k, "Percentage_Income_15k_20k" : list_15k_20k, "Percentage_Income_20k_30k" : list_20k_30k, "Percentage_Income_30k_40k" : list_30k_40k, "Percentage_Income_40k_50k" : list_40k_50k, "Percentage_Income_50k_60k" : list_50k_60k, "Percentage_Income_60k_75k" : list_60k_75k, "Percentage_Income_75k_100k" : list_75k_100k, "Percentage_Income_100k_150k" : list_100k_150k,  "Percentage_Income_150k_200k" : list_150k_200k, "Percentage_Income_over_200k" : list_over_200k, "Percentage_0_4_years" : list_0_4_years,"Percentage_5_9_years" : list_5_9_years, "Percentage_10_14_years" : list_10_14_years, "Percentage_15_17_years" : list_15_17_years, "Percentage_18_20_years" : list_18_20_years, "Percentage_21_24_years" : list_21_24_years, "Percentage_25_34_years" : list_25_34_years, "Percentage_35_44_years" : list_35_44_years, "Percentage_45_54_years" : list_45_54_years, "Percentage_55_59_years" : list_55_59_years, "Percentage_60_64_years" : list_60_64_years, "Percentage_65_74_years" : list_65_74_years, "Percentage_75_84_years" : list_75_84_years, "Percentage_over_85_years" : list_over_85_years, "Percentage_Independents_Previous_Presidential_Election" : list_previous_presidential_election_independants, "Count_Contributions_Democrats" : list_count_contributions_democrats, "Sum_Contributions_Democrats" : list_sum_contributions_democrats, "Count_Contributions_Republicans" : list_count_contributions_republicans,"Sum_Contributions_Republicans" : list_sum_contributions_republicans}
            #df_temp_new_col = pd.DataFrame(data_new_col)           
            
            #export definition data
            if i == 0:
                data_def = {"City" : list_city[i], "State" : list_state[i], 'Average_Precipitation' : list_rainfall_def, 'Average_Snowfall' : list_snowfall_def,'Average_Rainy_Days' : list_average_rainy_days_def, 'Average_Sunny_Days': list_average_sunny_days_def,'Average_High_Jul' : list_average_high_jul_def, 'Average_Low_Jan' : list_average_low_jan_def, 'Comfort_Index' : list_comfort_index_def, 'UV_Index' : list_uv_index_def, 'Elevation' : list_elevation_def, "Land_Area" : list_land_area_def, "Water_Area" : list_water_area_def,  "Cost_Living_Overall" : list_cost_of_living_overall_def, "Cost_Grocery" : list_cost_of_grocery_def, "Cost_Health" : list_cost_of_health_def, "Cost_Housing" : list_cost_of_housing_def, "Cost_Median_Home" : list_cost_of_median_home_cost_def, "Cost_Utilites" : list_cost_of_utilities_def, "Cost_Transportation" : list_cost_of_transportation_def, "Cost_Miscellaneous" : list_cost_of_miscellanous_def, "Count_Violent_Crimes" : list_violent_def, "Count_Murders" : list_murder_def, "Count_Rapes" : list_rape_def, "Count_Robberies" : list_robbery_def, "Count_Assaults" : list_assault_def, "Count_Property_Crimes" : list_property_def, "Count_Bulgaries" : list_bulgary_def, "Count_Larcenies" : list_larceny_def, "Count_Autos" : list_auto_def, "Index_Violent_Crimes" : list_index_violent_def, "Index_Property_Crimes" : list_index_property_def, "Overall_Expenses_Per_Student" : list_overall_expenses_per_student_def, "Education_Expenses_Per_Student" : list_education_expenses_per_student_def, "Instruction_Expenses_Per_Student" : list_instruction_expenses_per_student_def, "Count_Students_Per_Teacher" : list_student_per_teacher_def, "Count_Students_Per_Librarian" : list_students_per_librarian_def, "Count_Students_Per_Counselor" : list_students_per_counselor_def, "Percentage_Grade_School" : list_grade_school_def, "Percentage_Some_High_School" : list_some_high_school_def, "Percentage_High_School_Grad" : list_high_school_grad_def, "Percentage_High_School_Grad_Only" : list_high_school_grad_only_def, "Percentage_Some_College" : list_some_college_def, "Percentage_Degree_Two_Years" : list_degree_two_years_def, "Percentage_Degree_Four_Years" : list_degree_four_years_def, "Percentage_Degree_Four_Years_Only" : list_degree_four_year_only_def, "Percentage_Degree_Master" : list_degree_masters_def, "Percentage_Degree_Professional" : list_degree_professional_def, "Unemployment_Rate" : list_umemployment_rate_def, "Recent_Job_Growth" : list_recent_job_growth_def, "Future_Job_Growth" : list_future_job_growth_def, "Sales_Taxes" : list_sales_taxes_def, "Income_Tax" : list_income_tax_def, "Income_Per_Capita" : list_income_per_capita_def, "Household_Income" : list_household_income_def, "Family_Median_Income" : list_family_median_income_def, "Percentage_Income_Under_15k" : list_under_15k_def, "Percentage_Income_15k_20k" : list_15k_20k_def, "Percentage_Income_20k_30k" : list_20k_30k_def, "Percentage_Income_30k_40k" : list_30k_40k_def, "Percentage_Income_40k_50k" : list_40k_50k_def, "Percentage_Income_50k_60k" : list_50k_60k_def, "Percentage_Income_60k_75k" : list_60k_75k_def, "Percentage_Income_75k_100k" : list_75k_100k_def, "Percentage_Income_100k_150k" : list_100k_150k_def,  "Percentage_Income_150k_200k" : list_150k_200k_def, "Percentage_Income_over_200k" : list_over_200k_def,  "Population" : list_population_def, "Percentage_Female_Population" : list_female_population_def, "Percentage_Male_Population" : list_male_population_def, "Median_Age" : list_median_age_def, "Density_Population" : list_population_density_def, "Percentage_White_Population" : list_white_def, "Percentage_Black_Population" : list_black_def, "Percentage_Asian_Population" : list_asian_def, "Percentage_Native_American_Population" : list_native_american_def, "Percentage_Hawaiian_Pacific_Islander_Population" : list_hawaiian_pacific_islander_def, "Percentage_Other_Race_Population" : list_other_race_def, "Percentage_Two_Or_More_Races_Population" : list_two_or_more_races_def, "Percentage_Hispanic_Population" : list_hispanic_def, "Percentage_Married_Population" : list_married_population_def, "Percentage_Currently_Married_Population" : list_currently_married_def, "Percentage_Married_But_Seperated_Population" : list_married_but_seperated_def, "Percentage_Single_Population" : list_single_population_def, "Percentage_Never_Married_Population" : list_never_married_def, "Percentage_Divorced_Population" : list_divorced_def, "Percentage_Widowed_Population" : list_widowed_def, "Household_Size" : list_household_size_def, "Count_Households" : list_households_def, "Count_Family_Households" : list_family_households_def, "Percentage_Married_Couples_With_Children" : list_married_couple_with_children_def, "Percentage_Married_Couples_Without_Children" : list_married_couple_without_children_def, "Count_Non_Family_Households" : list_non_family_households_def, "Percentage_Single_Householder_With_Children" : list_single_householder_with_children_def, "Percentage_Single_Householder_Without_Children" : list_single_householder_without_children_def, "Percentage_0_4_years" : list_0_4_years_def,"Percentage_5_9_years" : list_5_9_years_def, "Percentage_10_14_years" : list_10_14_years_def, "Percentage_15_17_years" : list_15_17_years_def, "Percentage_18_20_years" : list_18_20_years_def, "Percentage_21_24_years" : list_21_24_years_def, "Percentage_25_34_years" : list_25_34_years_def, "Percentage_35_44_years" : list_35_44_years_def, "Percentage_45_54_years" : list_45_54_years_def, "Percentage_55_59_years" : list_55_59_years_def, "Percentage_60_64_years" : list_60_64_years_def, "Percentage_65_74_years" : list_65_74_years_def, "Percentage_75_84_years" : list_75_84_years_def, "Percentage_over_85_years" : list_over_85_years_def, "Count_Doctors_Per_100k_Pop" : list_doctor_per_100k_pop_def, "Cost_Health_Index" : list_cost_health_index_def, "Water_Index" : list_water_index_def, "Air_Index" : list_air_index_def, "Results_Previous_Presidential_Elections" : list_previous_presidential_elections_def, "Percentage_Democrats_Previous_Presidential_Election" :  list_previous_presidential_election_democrats_def, "Percentage_Republicans_Previous_Presidential_Election" : list_previous_presidential_election_republicans_def, "Percentage_Independents_Previous_Presidential_Election" : list_previous_presidential_election_independants_def, "Count_Contributions_Democrats" : list_count_contributions_democrats_def, "Sum_Contributions_Democrats" : list_sum_contributions_democrats_def, "Count_Contributions_Republicans" : list_count_contributions_republicans_def,"Sum_Contributions_Republicans" : list_sum_contributions_republicans_def, "Percentage_Religous" : list_religious_def, "Percentage_Baptist" : list_baptist_def, "Percentage_Episcopalian" : list_episcopalian_def, "Percentage_Catholic" : list_catholic_def , "Percentage_Lutheran" : list_lutheran_def, "Percentage_Methodologist" : list_methodist_def, "Percentage_Pentecostal" : list_pentecostal_def, "Percentage_Prebysterian" : list_pentecostal_def, "Percentage_Jesus_Christ" : list_jesus_christ_def, "Percentage_Christian" : list_christian_faith_def, "Percentage_Judaism" : list_jusdaism_def, "Percentage_Eastern_Faith" : list_eastern_faith_def, "Percentage_Islam" : list_islam_def, "Count_Number_Homes" :  list_number_homes_def, "Median_Home_Age" : list_median_home_age_def, "Median_Home_Cost" : list_median_home_cost_def, "Home_Appreciation_12_months" : list_home_appreciation_last_12_months_def, "Home_Appreciation_5_years" : list_home_appreciation_last_5_months_def, "Home_Appreciation_10_years" : list_home_appreciation_last_10_months_def, "Property_Tax_Rates" : list_property_tax_rates_def, "Average_Property_Tax_Paid" : list_property_tax_paid_def, "Percentage_Homes_Owned" : list_homes_owned_def, "Percentage_Homes_Vacant" : list_housing_vacant_def, "Percentage_Homes_Rented" : list_homes_rented_def, "Percentage_Vacant_For_Rent" : list_vacant_for_rent_def,  "Percentage_Vacant_Rented" :  list_vacant_rented_def, "Percentage_Vacant_For_Sale" : list_vacant_for_sale_def, "Percentage_Vacant_Sold" : list_vacant_sold_def, "Percentage_Vacant_For_Vacation" : list_vacant_vacation_def, "Percentage_Vacant_Other" : list_vacant_other_def,  "Percentage_Own_Occupied_House_Less_20K" : list_own_occupied_houses_less_than_20k_def, "Percentage_Own_Occupied_House_Between_20K_And_40K" :  list_own_occupied_houses_between_20k_and_40k_def, "Percentage_Own_Occupied_House_Between_40K_And_60K" :  list_own_occupied_houses_between_40k_and_60k_def, "Percentage_Own_Occupied_House_Between_60K_And_80K" :  list_own_occupied_houses_between_60k_and_80k_def, "Percentage_Own_Occupied_House_Between_80K_And_100K" :  list_own_occupied_houses_between_80k_and_100k_def, "Percentage_Own_Occupied_House_Between_100K_And_150K" :  list_own_occupied_houses_between_100k_and_150k_def, "Percentage_Own_Occupied_House_Between_150K_And_200K" :  list_own_occupied_houses_between_150k_and_200k_def, "Percentage_Own_Occupied_House_Between_200K_And_300K" :  list_own_occupied_houses_between_200k_and_300k_def, "Percentage_Own_Occupied_House_Between_300K_And_400K" :  list_own_occupied_houses_between_300k_and_400k_def, "Percentage_Own_Occupied_House_Between_400K_And_500K" :  list_own_occupied_houses_between_400k_and_500k_def, "Percentage_Own_Occupied_House_Between_500K_And_750K" :  list_own_occupied_houses_between_500k_and_750k_def, "Percentage_Own_Occupied_House_Between_750K_And_1000K" :  list_own_occupied_houses_between_750k_and_1000k_def, "Percentage_Own_Occupied_House_Between_1000K_And_1500K" :  list_own_occupied_houses_between_1000k_and_1500k_def, "Percentage_Own_Occupied_House_Between_1500K_And_2000K" :  list_own_occupied_houses_between_1500k_and_2000k_def, "Percentage_Own_Occupied_House_More_2000K" :  list_own_occupied_houses_more_than_2000k_def, "Percentage_Houses_Younger_2014" : list_housing_units_younger_than_2014_def,  "Percentage_Houses_Between_2010_And_2013" : list_housing_units_between_2010_and_2013_def, "Percentage_Houses_Between_2000_And_2009" : list_housing_units_between_2000_and_2009_def, "Percentage_Houses_Between_1990_And_1999" : list_housing_units_between_1990_and_1999_def, "Percentage_Houses_Between_1980_And_1989" : list_housing_units_between_1980_and_1989_def, "Percentage_Houses_Between_1970_And_1979" : list_housing_units_between_1970_and_1979_def, "Percentage_Houses_Between_1960_And_1969" : list_housing_units_between_1960_and_1969_def, "Percentage_Houses_Between_1950_And_1959" : list_housing_units_between_1950_and_1959_def, "Percentage_Houses_Between_1940_And_1949" : list_housing_units_between_1940_and_1949_def, "Percentage_Houses_Older_1949" : list_housing_units_older_than_1939_def, "Commute_Time_Minute" : list_commute_time_def, "Percentage_Commute_Auto_Alone" : list_commute_auto_alone_def, "Percentage_Commute_Carpool" : list_commute_carpool_def, "Percentage_Commute_Mass_Transit" :  list_commute_mass_transit_def, "Percentage_Commute_Bicycle" : list_commute_bicycle_def, "Percentage_Commute_Walk" : list_commute_walk_def}      
                df_def = pd.DataFrame(data_def)
        
  
            #logic based on index
            if N == 0:
                df_final = df_temp
            else:
                df_final = pd.concat([df_final, df_temp])
            
            N = N + 1
                
        
            df_final.to_excel("Top_US_Cities_Data_V{}.xlsx".format(x))
            #df_city.to_excel("List_US_Cities.xlsx")
            #df_column.to_excel("List_Columns.xlsx")
            #df_final.to_excel("New_Columns_{}.xlsx".format(x))

            if i == 0:
                df_def.to_excel("Definitions.xlsx")               
    
    except Exception as e:
        
        list_failures.append(list_city_state_v2[i])
        print("Failure for {}, {}".format(list_city[i],list_state[i]))
        print(e)
            

    #data_failures = {'City' : list_failures}
    #df_failures = pd.DataFrame(data_failures)
    #df_failures.to_excel("Failures_{}.xlsx".format(x))
  
#main(True,0,1,1)


#multiprocessing using 2 cores 
#if __name__ == '__main__':
    
    #print('Start Multiprocessing')
    #proc1 = Process(target = main, args=(True,0,1,1))
    #proc1.start()
    
    #proc2 = Process(target = main , args=(True,1,2,2))
    #proc2.start()
    
    #proc1.join()
    #proc2.join()


    #print('End Multiprocessing - All tasks are completed')

for key in data.keys():
   print(key)
   print(len(data[key]))
