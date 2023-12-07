import random
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from pymongo import MongoClient
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import requests
import csv
from io import StringIO

client = MongoClient("mongodb://34.125.160.112/gpuzone")
db = client['gpuzone']
gpu_collection = db['gpu']


response = requests.get('https://www.userbenchmark.com/resources/download/csv/GPU_UserBenchmarks.csv')
gpu_list = []
# Check if the request was successful
if response.status_code == 200:
    # Use StringIO to treat the CSV text as a file
    csvfile = StringIO(response.text)

    # Create a DictReader to parse the CSV
    reader = csv.DictReader(csvfile)

    # Loop through the rows in the CSV
    for row in reader:
        # Extract only the desired fields and add them to the list
        gpu_list.append({
            'brand': row['Brand'],  # Replace with your actual CSV header names
            'model': row['Model'],
            'rank': row['Rank'],
            'url': row['URL'],
            'part_number': row['Part Number'],
        })
else:
    print(f"Failed to download CSV: Status code {response.status_code}")

unique_values = set()
unique_gpus = []
for d in gpu_list:
    # Check if the key exists in the dictionary
    if 'url' in d:
        value = d['url']
        # Add the dictionary to the result if the value is unique
        if value not in unique_values:
            unique_gpus.append(d)
            unique_values.add(value)
proxy_list = []

# Open the file and read each line
with open('proxies_list.txt', 'r') as file:
    for line in file:
        proxy_list.append(line.strip())

file.close()

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
previous_url = None
for gpu in unique_gpus:
    count = 0
    print("Scraping " + gpu['url'])
    if previous_url == gpu['url'] and success:
        print("Duplicate URL found. Skipping... ")
        new_gpu = gpu
        new_gpu['image_url'] = current_gpu['image_url']
        new_gpu['release_date'] = current_gpu['release_date']
        new_gpu['description'] = current_gpu['description']
        new_gpu['features'] = current_gpu['features']
        query = {'model': current_gpu['model']}
        update = {'$set': current_gpu}
        gpu_collection.update_one(query, update, upsert=True)
        previous_url = current_gpu['url']
        print("successfully updated")
        success = True
        continue
    success = False
    current_gpu = gpu
    previous_url = current_gpu['url']
    while not success:
        if count == 3:
            print("Tried 3 times. Failed to scrape, skipping...")
            break
        try:
            driver = create_firefox_driver_with_authenticated_proxy()
            driver.get(gpu['url'])
            sleep(5)
            # Find the image by class name
            image = driver.find_element(By.CSS_SELECTOR, '.lazy.mhajaxstatus.ptimg')
            # Assuming you want to extract the 'src' attribute of the first matched image
            if image:
                image_url = image.get_attribute('src')
                current_gpu['image_url'] = image_url
            else:
                current_gpu['image_url'] = 'No image'

            release_date_element = driver.find_element(By.CSS_SELECTOR, '.cmp-cpt.tallp.cmp-cpt-l')
            if release_date_element:
                current_gpu['release_date'] = release_date_element.text
            else:
                print("No element with the specified classes was found.")
            description_element = driver.find_element(By.CSS_SELECTOR, '.tallp.fl-dc.two-cols')
            # Assuming you want to extract the 'src' attribute of the first matched image
            if description_element:
                current_gpu['description'] = description_element.text
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
            current_gpu['features'] = h4_texts
            success = True
            driver.quit()
            previous_url = current_gpu['url']
            print("Successfully scraped")
        except:
            count += 1
            driver.quit()
            print("Failed... Trying again...")
            success = False
    query = {'model': current_gpu['model']}
    update = {'$set': current_gpu}
    gpu_collection.update_one(query, update, upsert=True)
