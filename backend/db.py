import random
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from pymongo import MongoClient
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import requests
import sys
from io import StringIO
sys.stdout.reconfigure(encoding='utf-8')

proxy_list = []
with open('proxies_list.txt', 'r') as file:
    for line in file:
        proxy_list.append(line.strip())

def pick_random_proxy(proxy_list):
    return random.choice(proxy_list)

def create_firefox_driver_with_authenticated_proxy():
    options = FirefoxOptions()
    proxy = pick_random_proxy(proxy_list) # Pick a random proxy
    proxy_host = proxy.split(':')[0]
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.http", proxy_host)
    options.set_preference("network.proxy.http_port", 80)
    options.set_preference("network.proxy.ssl", proxy_host)
    options.set_preference("network.proxy.ssl_port", 80)
    options.set_preference("network.proxy.no_proxies_on", "localhost, 127.0.0.1")
    options.add_argument("--headless")  # This sets the headless option

    # This method of authentication may not be supported
    options.set_preference("network.proxy.username", 'xwblikdv')
    options.set_preference("network.proxy.password", 'zmzz7nshpsdf')

    # Additional preferences to try avoiding the authentication dialog
    options.set_preference("signon.autologin.proxy", True)

    driver = webdriver.Firefox(options=options)

    return driver
gpu = {'url' : 'https://gpu.userbenchmark.com/Nvidia-RTX-4090/Rating/4136'}
driver = create_firefox_driver_with_authenticated_proxy()
driver.get(gpu['url'])
print(driver.page_source)
print("Scraping " + gpu['url'])
sleep(5)
# Find the image by class name
image = driver.find_element(By.CSS_SELECTOR, '.lazy.mhajaxstatus.ptimg')
# Assuming you want to extract the 'src' attribute of the first matched image
if image:
    image_url = image.get_attribute('src')
    gpu['image_url'] = image_url
    # print(image_url)
else:
    gpu['image_url'] = 'No image'

release_date_element = driver.find_element(By.CSS_SELECTOR, '.cmp-cpt.tallp.cmp-cpt-l')
if release_date_element:
    gpu['release_date'] = release_date_element.text
else:
    print("No element with the specified classes was found.")
description_element = driver.find_element(By.CSS_SELECTOR, '.tallp.fl-dc.two-cols')
# Assuming you want to extract the 'src' attribute of the first matched image
if description_element:
    gpu['description'] = description_element.text
    # print(desciption)
else:
    print("No element with the specified classes was found.")
    driver.quit()
features_elements = driver.find_element(By.CSS_SELECTOR, '.row.medp.chapt-m-t')
h4s = features_elements.find_elements(By.CSS_SELECTOR, '.col-xs-4')
h4_texts = {}
for features in h4s:
        h4_list = features.find_elements(By.TAG_NAME, 'h4')
        for h4 in h4_list:
            h4_text = h4.text
            # The following sibling can be a bit tricky since we don't have a direct way to do this in Selenium
            # One way to achieve it is to use JavaScript execution to return the next sibling's text
            following_text = driver.execute_script(
                "return arguments[0].nextSibling.textContent;", h4).strip()
            h4_texts[h4_text] = following_text
gpu['features'] = h4_texts