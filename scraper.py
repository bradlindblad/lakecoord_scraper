
# MODULES
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# START SELENIUM
chrome_path = "C:\\Program Files\\Chromedriver\\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.get("http://www.lat-long.com/Search.cfm?q=&State=ND&County=&FeatureType=lake")
time.sleep(2)

# DEF FNs and BUILD DATA FRAME
start = {'Lake': ['Lake name'],
         'Lat': [47.2],
         'Lon': [-99.1],
         'Cnty': 'Cass'}
mydata = pd.DataFrame(start)

# Loop begins
p = 0
while p < 40:

    sp = 0
    while sp < 20:
        # GET ACTUAL DATA FROM SUB PAGE
        # Find Lat and Lon
        driver.find_elements_by_css_selector("tr+ tr font > a")[sp].click()
        coords = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/font/table/tbody/"  # grab the Lat and Lon
                                            "tr/td[1]/table[1]/tbody/tr/td[1]/table/tbody/"
                                            "tr[2]/td/table/tbody/tr/td[1]/font[2]/p/font[2]").text
        coords = re.findall(r'\d+', coords)
        new_lat = str(coords[0] + '.' + coords[1])
        new_lon = str('-' + coords[2] + '.' + coords[3])  # create new lat and lon to be appended

        # Find Lake Name
        lake = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/font/table/tbody/tr/td[1]/"
                                     "table[1]/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/h1").text
        new_lake = lake.replace(", ND", "")

        # Find county name
        county = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/font/table/tbody/tr/td[1]"
                                              "/table[1]/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/"
                                              "tr/td[1]/font/strong[3]").text
        new_county = county

        mydata = mydata.append({'Lake': new_lake,
                      'Lat': new_lat,
                      'Lon': new_lon,
                      'Cnty': new_county}, ignore_index=True)

        sp = sp + 1
        driver.back()

    # Click Next 20
    try:
        driver.find_element_by_link_text("Next 20").click()
    except:
        pass
    try:
        driver.find_element_by_link_text("Next 9").click()
    except:
        pass
    p = p + 1

driver.close()

mydata.to_csv("lakes.csv", sep='\t')
