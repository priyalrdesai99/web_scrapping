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



#function for starting the driver
def startDriver(path):
    driver = webdriver.Chrome(path)
    driver.get('https://www.barchart.com/stocks/quotes/GOOG/competitors')
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
    #driver.get(driver.getCurrentURL())
    driver.refresh()
    time.sleep(30)
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//footer')))
    temp = 0 
 #   try:
  #      #checking if there are more pages then load all the pages
        #print("Hello1")
         
   #     element = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.linkText, 'Show all')))
        
    #    driver.find_element_by_link_text("Show all").click()
     #   time.wait(25)
      #  element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//footer')))
#       element.click()
       # print("Inside show all")        
    #except:
     #   a = 0 
      #  print(a)
    try:
        data = scrapData(driver,data)
        while(driver.find_element_by_class_name("next")):
            driver.find_element_by_class_name("next").click()
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//footer')))
            data = scrapData(driver,data)
            
            
            print(temp)
        
    except:
        a = 0
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//footer')))
        
    print(len(data))
    return(data)




#getting reference of the dropdown
def getDropDownList(driver):
    return(Select(driver.find_element_by_id("competitors-quote-sectors")))


#getting the input and output file

def main(argv):
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


#main line of code 


if __name__ == "__main__":
    #print(len(sys.argv))
    if(len(sys.argv) <= 1):
        input_file_path = './input_of_symbols.txt'
        output_file_path =  './output_file.json'
    else:
        input_file_path,output_file_path = main(sys.argv[1:])
    
        
    
    driver_path = './chromedriver'
    option = "Indices S&P 500"

    driver = startDriver(driver_path)
    dropdown_items = getDropDownList(driver)
    data = getWholeData(dropdown_items,driver,option)
    
    
    
    #print(len(data))
    #reading the file
    input_file = open(input_file_path)
    file_data = input_file.read().split(",")
    try:
        ans_in_json = json.dumps([{i:data[i]} for i in file_data],indent = 4)
        print(ans_in_json)
        with open(output_file_path, "w") as outfile: 
            outfile.write(ans_in_json) 

    except:
        print("Data not found")

    






