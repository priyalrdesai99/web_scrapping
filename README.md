# web_scrapping
 An application which scraps the Symbols and their Names from the url given in configuration file and gives the Name of the desired Symbols inputted through file in Json format.

Files:

webscrapping.py: It contains code required for scrapping the data and converting the inputted Symbols to Json format.
test_scrapper.py: It contains code for unit testing.
config.ini: It is a configuration file 

input_of_symbols.txt: It is a file which is needed to be provided as input by default.
output_file.json: It is a file which is needed to be provided as output file by default.
chromedriver.exe: Is is a web driver.
run.sh: It contains the shell script for running test_scrapper.py and webscrapping.py files.


Information about configuration file:

website_url:The url to be used for scraping.
select_option_for_data: The option needed to be selected for getting the data.By default it is Indices S&P 500.
path_of_driver: It specifies the path of webchrome driver.
