import unittest

from webscrapping import *


class TestParseFunction(unittest.TestCase):
    option = ''
    website_url = ''
    path_of_driver = ''
    input_file = ''
    out_file = ''
    global driver
    dropdown_items = ''
    global web_page_data
    data_from_file = ''
    

    def test_ConfigParams(self):
        global driver
        global web_page_data
        self.assertEqual(1,1)
        self.option = 'Indices S&P 500'
        self.website_url = 'https://www.barchart.com/stocks/quotes/GOOG/competitors'
        self.path_of_driver = './chromedriver.exe'
        self.assertEqual(getconfigparams(),(self.website_url,self.option,self.path_of_driver))
        
        driver = startDriver(self.path_of_driver,self.website_url)
        self.dropdown_items = getDropDownList(driver)
        web_page_data = getWholeData(self.dropdown_items,driver,'Indices S&P 500')
        driver.close()
        
    
    def setUp(self):
        
        self.input_file,self.out_file = getfilenames(['-i','./input_of_symbols.txt','-o','./output_file.json'])
        
        self.data_from_file = getDatafromFile('./input_of_symbols.txt')
    
    def test_filename_is_not_none(self):
        self.assertIsNotNone(self.input_file)
        self.assertIsNotNone(self.out_file)
    
    def test_data_from_file_is_not_none(self):
        self.assertIsNotNone(self.data_from_file)
      
        
    def testfiledata(self):
        
        self.assertEqual(self.data_from_file,['AAPL','GOOG','MSFT'])
        
        
    def test_dataset_is_a_dict(self):
        global web_page_data
        self.assertTrue(isinstance(web_page_data, dict))
        
        
        
        
        
        
    
    

if __name__ == '__main__':
    unittest.main()