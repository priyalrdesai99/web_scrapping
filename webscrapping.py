#!/usr/bin/env python
# coding: utf-8


#importing selnium and required things 

import json
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys,getopt
from configparser import ConfigParser 




#function for starting the driver
def startDriver(path,website_url):
    driver = webdriver.Chrome(path)
    driver.get(website_url)
    return(driver)


#scrapping the visible data 

def scrapData(driver,data):
    delay = 100
    #time.sleep(100)
    table_data = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//tbody')))
    x = table_data.text.split("\n")
    i = 0
    while(i < len(x)):
        data[x[i]] = x[i+1]
        i = i+10
    return(data)        



#getting the data based on the option selected
def getWholeData(select_box,driver,text):
    data = {}
    select_box.select_by_visible_text(text)
    time.sleep(5)
    driver.refresh()
    time.sleep(30)
   # element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//footer')))
    
    try:
        data = scrapData(driver,data)
        while(driver.find_element_by_class_name("next")):
            driver.find_element_by_class_name("next").click()
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//footer')))
            data = scrapData(driver,data)
    except:
        a = 0
    
        
    #print(len(data))
    return(data)




#getting reference of the dropdown
def getDropDownList(driver):
    return(Select(driver.find_element_by_id("competitors-quote-sectors")))


#getting the input and output file

def getfilenames(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      return(0)
   for opt, arg in opts:
      if opt == '-h':
         print("No command line passed")
         return(0)
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   return(inputfile,outputfile)


def getconfigparams():
    config = ConfigParser() 
    config.read('config.ini')
    
    try:
        website_url = config.get('information','website_url')
    except NoOptionError:
        website_url = 'https://www.barchart.com/stocks/quotes/GOOG/competitors'
    
    try:
        option = config.get('information','select_option_for_data')
    except NoOptionError:
        option = 'Indices S&P 500'
        
    try:
        driver_path = config.get('information','path_of_driver')
    except NoOptionError:
        driver_path = './chromedriver.exe'

    return(website_url,option,driver_path)


def getJsonData(data,file_data):
    
    try:
        ans_in_json = json.dumps([{i:data[i] if(i in data.keys()) else "Value not found"} for i in file_data],indent = 4)
        print(ans_in_json)

    except:
        print("Data not found")
    return(ans_in_json)



def getDatafromFile(input_file_path):
    input_file = open(input_file_path)
    file_data = input_file.read().split(",")
    input_file.close()
    return(file_data)


#main line of code 


if __name__ == "__main__":
    #print(len(sys.argv))
    if(len(sys.argv) <= 1):
        input_file_path = './input_of_symbols.txt'
        output_file_path =  './output_file.json'
    else:
        input_file_path,output_file_path = getfilenames(sys.argv[1:])
    
    #getting data from config file
    
    website_url,option,driver_path = getconfigparams()
    
    
    driver = startDriver(driver_path,website_url)
    dropdown_items = getDropDownList(driver)
    data = getWholeData(dropdown_items,driver,option)
    
    
    
    print(len(data))
    #reading the data from the file
    file_data = getDatafromFile(input_file_path)
    
    ans_in_json = getJsonData(data,file_data)
    
    with open(output_file_path, "w") as outfile: 
        outfile.write(ans_in_json) 

    
    
    driver.close()





