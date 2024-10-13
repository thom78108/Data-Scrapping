#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 14:20:30 2023

@author: elizabethtnguyen
"""

#import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re                  
import requests
import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
from urllib.request import urlopen
from lxml import html
import ssl

#code 1
#print where is perm file
print(requests.certs.where())
#pull html with beautifulsoup       
webpage = requests.get("https://www.bestplaces.net/religion/city/illinois/chicago", verify = '/Users/elizabethtnguyen/Desktop/Thomas/bestplaces.cer')
soup = webpage.read().decode('utf8')
#print where is perm file again
import ssl
print(ssl.OPENSSL_VERSION)

#code 2
import ssl
context = ssl._create_unverified_context()
fp = urllib.request.urlopen("https://www.bestplaces.net/climate/city/illinois/chicago",context=context)
soup = BeautifulSoup(fp, "html.parser")
body = soup.find("body")
dom = etree.HTML(str(body))
print(dom.xpath('//*[@id="mainContent_dgClimate"]/tr[3]/td[2]')[0].text)
print(dom.xpath("//*[@id='mainContent_dgClimate']/tr[5]/td[1]/button")[0].attrib["title"])

#code 3
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
urllib2.urlopen("https://www.bestplaces.net/religion/city/illinois/chicago").read()

#code 4
list_rainfall = []
context = ssl._create_unverified_context()
response = urlopen("https://www.bestplaces.net/climate/city/illinois/chicago")
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)
print(tree)
print(tree.xpath('//*[@id="mainContent_dgClimate"]/tbody/tr[2]/td[2]'))

#code 5
list_rainfall = []
context = ssl._create_unverified_context()
response = urlopen("https://www.bestplaces.net/climate/city/illinois/chicago")
encoding = response.headers.get_content_charset()
output = response.read().decode(encoding)
htmltree = html.fromstring(output)


print(htmltree.xpath('//*[@id="mainContent_dgClimate"]/tbody/tr[2]/td[2]'))
list_rainfall.append(output)
data_failures = {'Test' : list_rainfall}
df_failures = pd.DataFrame(data_failures)
df_failures.to_excel("Test.xlsx")

#code 6
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path="/Users/elizabethtnguyen/Desktop/Thomas/chromedriver")
driver.set_window_position(0,0)
driver.set_window_size(0,0)
driver.get("https://www.bestplaces.net/climate/city/illinois/chicago")
html = driver.page_source
print(html)



#pull html
context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/health/city/illinois/chicago")
soup = BeautifulSoup(page_source, "html.parser")
body = soup.find("body")
dom = etree.HTML(str(body))

#pull health data          
value = dom.xpath("/html/body/form/div[7]/div[1]/div[2]")[0]
list_doctor_per_100k_pop.append(int(re.search(r'\d+', value).group()))
value = dom.xpath("//*[@id='form1']/div[7]/div[2]/div[2]/div[3]")[0].text
list_cost_health_index.append(convert_str_to_float(value.replace(" / 100", "")))
value = dom.xpath("//*[@id='form1']/div[7]/div[2]/div[2]/div[4]")[0].text
list_water_index.append(convert_str_to_float(value.replace(" / 100", "")))
value = dom.xpath("//*[@id='form1']/div[7]/div[2]/div[2]/div[6]")
list_air_index.append(convert_str_to_float(value.replace(" / 100", "")))

str(≈[3]).split('There are')[1].split('physicians')[0].replace(' ','')
str(soup.find_all(class_="row")[3]).split('The annual BestPlaces Health Cost Index for the Chicago area is')[1].split('(lower=better)')[0].replace(' ','')
str(soup.find_all(class_="row")[3]).split('The annual BestPlaces Water Quality Index for the Chicago area is')[1].split('(100=best')[0].replace(' ','')
str(soup.find_all(≈="row")[3]).split('The annual BestPlaces Air Quality Index for the Chicago area is')[1].split('(100=best')[0].replace(' ','')

str(soup.find_all(class_="card-body m-0 p-0")[0]).split('data: ')[1].split(", ")[0].split(",")


//*[@id="form1"]/div[7]/div[2]/div[2]/p[1]/text()
//*[@id="form1"]/div[7]/div[2]/div[2]/div[2]/div

context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/education/city/illinois/chicago")
soup = BeautifulSoup(page_source, "html.parser")
value = str(soup.find_all(class_="card-body m-0 p-0")[0]).split('data: ')[1].split("[")[1].split("]")[0]
list_temp = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))
     
context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/religion/city/illinois/chicago")
soup = BeautifulSoup(page_source, "html.parser")
body = soup.find("body")
body = soup.find("body")
dom = etree.HTML(str(body))
value = str(soup.find_all(class_="col-md-12")[1])
list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))

#pull html
context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/crime/city/nebraska/abie")
soup = BeautifulSoup(page_source, "html.parser")
body = soup.find("body")
dom = etree.HTML(str(body))
value = str(soup.find_all(class_="col-md-12")[1])
list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value))
value = dom.xpath("//*[@id='example']/tr[1]/td[2]")[0].text
//*[@id="example"]/tbody/tr[1]/td[2]
value = str(soup).split("tbody")[1]
if int("2") in list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value))):
    print("salut bill")

context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/voting/city/nebraska/abie")
soup = BeautifulSoup(page_source, "html.parser")
body = soup.find("body")
value = str(soup.find_all(class_="col-md-12")[1])
list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))

value = str(soup.find_all(class_="font-weight-bold")[2]).split("{}".format(list_city[i]))[1].replace("</h5>",'').replace(": ","")
list_previous_presidential_elections.append(value)

list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value))
value = dom.xpath("//*[@id='form1']/div[7]/div[2]/div[2]/div[2]/div/p[8]/text()[1]")
value = str(soup.find_tag(tag="[b]")
value = str(soup.find_all("p")[11])
list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))

list_previous_presidential_election_democrats = []
value = str(soup.find_all(class_="col-md-12")[1])
list_temp = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))
list_previous_presidential_election_democrats.append(list_temp[1])

context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/transportation/city/nebraska/abie")
soup = BeautifulSoup(page_source, "html.parser")
body = soup.find("body")
value = str(soup.find_all(class_="col-md-12")[1])
list_temp = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))

#pull html
context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/crime/city/nebraska/anoka")
soup = BeautifulSoup(page_source, "html.parser")      
value = str(soup).split("tbody")[1]
list_temp = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))

#pull html
context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/economy/city/alabama/abanda")
soup = BeautifulSoup(page_source, "html.parser")
body = soup.find("body")
dom = etree.HTML(str(body))

#pull economy data
value = dom.xpath("//*[@id='mainContent_dgEconomy']/tr[2]/td[2]")[0].text
list_umemployment_rate.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgEconomy']/tr[3]/td[2]")[0].text
list_recent_job_growth.append(convert_str_to_float(value))      
value = dom.xpath("//*[@id='mainContent_dgEconomy']/tr[4]/td[2]")[0].text
list_future_job_growth.append(convert_str_to_float(value))  
value = dom.xpath("//*[@id='mainContent_dgEconomy']/tr[5]/td[2]")[0].text
list_sales_taxes.append(convert_str_to_float(value)) 
value = dom.xpath("//*[@id='mainContent_dgEconomy']/tr[6]/td[2]")[0].text
list_income_tax.append(convert_str_to_float(value))  
value = dom.xpath("//*[@id='mainContent_dgEconomy']/tr[7]/td[2]")[0].text
list_income_per_capita.append(convert_str_to_float(value))  
value = dom.xpath("//*[@id='mainContent_dgEconomy']/tr[8]/td[2]")[0].text
list_household_income.append(convert_str_to_float(value))  
value = dom.xpath("//*[@id='mainContent_dgEconomy']/tr[9]/td[2]")[0].text
list_family_median_income.append(convert_str_to_float(value)) 

context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/health/city/alabama/coats_bend")
soup = BeautifulSoup(page_source, "html.parser")
body = soup.find("body")
dom = etree.HTML(str(body))

#pull health data          
value = str(soup.find_all(class_="row")[3]).split('There are')[1].split('physicians')[0].replace(' ','')
list_doctor_per_100k_pop.append(int(re.search(r'\d+', value).group()))
value = str(soup.find_all(class_="row")[3]).split('The annual BestPlaces Health Cost Index for the coats bend area is')[1].split('(lower=better)')[0].replace(' ','')

context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/education/city/alaska/game_creek")
soup = BeautifulSoup(page_source, "html.parser")
body = soup.find("body")
dom = etree.HTML(str(body))


#pull education data
value = dom.xpath("//*[@id='mainContent_dgEducation']/tr[2]/td[2]")[0].text
list_overall_expenses_per_student.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgEducation']/tr[3]/td[2]")[0].text
list_education_expenses_per_student.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgEducation']/tr[4]/td[2]")[0].text
list_instruction_expenses_per_student.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgEducation']/tr[5]/td[2]")[0].text
list_student_per_teacher.append(convert_str_to_float(value))               
value = dom.xpath("//*[@id='mainContent_dgEducation']/tr[6]/td[2]")[0].text
list_students_per_librarian.append(convert_str_to_float(value))   
value = dom.xpath("//*[@id='mainContent_dgEducation']/tr[7]/td[2]")[0].text
list_students_per_counselor.append(convert_str_to_float(value)) 

value = str(soup.find_all(class_="card-body m-0 p-0")[0]).split('data: ')[1].split("[")[1].split("]")[0]
list_education_distribution = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))
list_grade_school.append(list_education_distribution[0])         
list_some_high_school.append(list_education_distribution[1])       
list_high_school_grad.append(list_education_distribution[2])       
list_high_school_grad_only.append(list_education_distribution[3])       
list_some_college.append(list_education_distribution[4])       
list_degree_two_years.append(list_education_distribution[5])       
list_degree_four_years.append(list_education_distribution[6])       
list_degree_four_year_only.append(list_education_distribution[7])       
list_degree_masters.append(list_education_distribution[8])       
list_degree_professional.append(list_education_distribution[9]) 

#pull html
context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/people/city/arizona/chiawuli_tak".format(list_state[i],list_city[i]),context=context)
soup = BeautifulSoup(page_source, "html.parser")
body = soup.find("body")
dom = etree.HTML(str(body))

#pull people data
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[2]/td[2]")[0].text
list_population.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[3]/td[2]")[0].text
list_female_population.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[4]/td[2]")[0].text
list_male_population.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[5]/td[2]")[0].text
list_median_age.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[14]/td[2]")[0].text
list_population_density.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[15]/td[2]")[0].text
list_land_area.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[16]/td[2]")[0].text
list_water_area.append(convert_str_to_float(value))

#pull race data
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[18]/td[2]")[0].text
list_white.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[19]/td[2]")[0].text
list_black.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[20]/td[2]")[0].text
list_asian.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[21]/td[2]")[0].text
list_native_american.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[22]/td[2]")[0].text
list_hawaiian_pacific_islander.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[23]/td[2]")[0].text
list_other_race.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[24]/td[2]")[0].text
list_two_or_more_races.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[25]/td[2]")[0].text
list_hispanic.append(convert_str_to_float(value))

    
#pull marriage & family data
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[27]/td[2]")[0].text
list_married_population.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[28]/td[2]")[0].text
list_currently_married.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[29]/td[2]")[0].text
list_married_but_seperated.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[30]/td[2]")[0].text
list_single_population.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[31]/td[2]")[0].text
list_never_married.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[32]/td[2]")[0].text
list_divorced.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[33]/td[2]")[0].text
list_widowed.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[35]/td[2]")[0].text
list_household_size.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[36]/td[2]")[0].text
list_households.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[37]/td[2]")[0].text
list_family_households.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[38]/td[2]")[0].text
list_married_couple_with_children.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[39]/td[2]")[0].text
list_married_couple_without_children.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[40]/td[2]")[0].text
list_non_family_households.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[41]/td[2]")[0].text
list_single_householder_with_children.append(convert_str_to_float(value))
value = dom.xpath("//*[@id='mainContent_dgPeople']/tr[42]/td[2]")[0].text
list_single_householder_without_children.append(convert_str_to_float(value))
   
#people distribution
value = str(soup.find_all(class_="card-body m-0 p-0")[0]).split('data: ')[1].split("[")[1].split("]")[0]
list_age_distribution = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))
list_0_4_years.append(list_age_distribution[0])         
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
list_over_85_years.append(list_age_distribution[13]) 


context = ssl._create_unverified_context()
page_source = urllib.request.urlopen("https://www.bestplaces.net/crime/city/illinois/chicago",context=context)
soup = BeautifulSoup(page_source, "html.parser")      
value = str(soup).split("tbody")[1]
list_temp = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))


#pull indexes for violent crimes and property crimes
try:
    value = str(soup.find_all(class_="col-md-12")[1])
    list_temp = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", value)))
    list_index_violent.append(list_temp[1])
    list_index_property.append(list_temp[3])
except:
    list_index_violent.append("N/A")
    list_index_property.append("N/A")


                