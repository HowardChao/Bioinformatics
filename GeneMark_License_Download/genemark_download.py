from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import gzip
import os

# 1. Install selenium 
# 2. Chrome's setting (chromedrive location)
# 3. Change the location  ==> a.chromedrive  b.download gm_key_64.gz path  c.write gm_key_64.gz path

# Create the Firefox WebDriver (/path/of/chromedrive)
driver = webdriver.Chrome('/Users/Kuan-Hao/Desktop/chromedriver')
driver.get("http://topaz.gatech.edu/GeneMark/license_download.cgi")
# If the browser is still running ~ wait ~otherwise ~ skip!
driver.implicitly_wait(5)

# Select GeneMarkS v.4.30
software_select = driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/form[1]/table/tbody/tr[3]/td/input[@type='radio']")
software_select.click()
# Select Linux_64
operating_system_select = driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/form[1]/table/tbody/tr[3]/td[2]/input[2]")
operating_system_select.click()

# Name 
name_text = driver.find_element_by_css_selector("center tr:nth-child(1) input")
name_text.send_keys("Howard Chao")
# Institution
institution_text = driver.find_element_by_css_selector("center tr:nth-child(2) input")
institution_text.send_keys("National Taiwan University")
# Country
country_text = driver.find_element_by_css_selector("center tr:nth-child(6) input")
country_text.send_keys("Taiwan")
# Email
email_text = driver.find_element_by_css_selector("center tr:nth-child(7) input")
email_text.send_keys("ntueeb05howard@gmail.com")

# Submit the form
form = driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/form[1]/center[4]/input[@id='submit']")
form.click()

# Wait for website to reload
driver.implicitly_wait(5)

# Download
download_button = driver.find_element_by_xpath("html/body/table/tbody/tr[2]/td/center[7]/a[2]")
driver.get(download_button.get_attribute("href"))
# Close browser
driver.close()

# Unzip and write to gm_key_64.txt
with gzip.open('/Users/Kuan-Hao/Downloads/gm_key_64.gz', 'rb') as f:
    file_content = f.read()
f = open('/Users/Kuan-Hao/Downloads/gm_key_64.txt', 'wb')
f.write(file_content)
f.close()
os.remove('/Users/Kuan-Hao/Downloads/gm_key_64.gz')

