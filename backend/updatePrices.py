from datetime import datetime, timedelta
from http.client import HTTPException
import random
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

client = MongoClient("mongodb://34.125.160.112/gpuzone")
db = client['gpuzone']
price_collection = db['price']
gpu_collection = db['gpu']
class SearchRequest(BaseModel):
    search_term: str

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


website_info = {
    'amazon': {
        'product': 'div[data-component-type="s-search-result"]',
        'name': 'span.a-size-medium',
        'price': 'span.a-price-whole',
        'link': 'a.a-link-normal',
        'image': 'img.s-image',
        'base_url': 'https://www.amazon.com/s?k=',
        'separator': '+'
    }
}

def get_random_timestamp():
    # Current date
    current_date = datetime.now()

    # 30 days before the current date
    month_ago = current_date - timedelta(days=30)

    # Generate a random timestamp within the last 30 days
    random_timestamp = month_ago + timedelta(seconds=random.randint(0, 30 * 24 * 3600))

    return random_timestamp


def duplicate_add(price_data):
    results = []
    base = price_data['price']
    # extract the number from the string
    base = base.replace('$', '')
    base = base.replace(',', '')
    try:
        base = float(base)
        # increase or decrease the price by random amount up to 10%
        for i in range(50):
            new_price_data = price_data.copy()
            new_price_data['price'] = round(base + base * random.uniform(-0.1, 0.1), 2)
            # change the timestamp to a random time within the last month
            new_price_data['timestamp'] = get_random_timestamp()
            new_price_data.pop('_id', None)
            price_collection.insert_one(new_price_data)
    except ValueError:
        print("Not a number")

def get_prices(request_body: SearchRequest):
    search_term = request_body.search_term
    keywords = search_term.split(' ')
    keywords = [keyword.lower() for keyword in keywords]
    print(keywords)
    results = []
    for store in website_info.keys():
        print("Searching " + store)
        info = website_info[store]
        driver = create_firefox_driver_with_authenticated_proxy()

        search_term1 = search_term.replace(' ', info['separator'])
        if store == 'ebay':
            search_term1 += '&_sacat=0'
        print(info['base_url'] + search_term1)
        driver.get(info['base_url'] + search_term1)
        try:
            # Locate all item cells
            item_cells = driver.find_elements(By.CSS_SELECTOR, info['product'])
            for item in item_cells:
                # Fetch product name
                try:
                    product_name = item.find_element(By.CSS_SELECTOR, info['name']).text
                except NoSuchElementException:
                    product_name = "Not found"
                # Fetch product link
                try:
                    product_link = item.find_element(By.CSS_SELECTOR, info['link']).get_attribute('href')
                except NoSuchElementException:
                    product_link = "Not found"
                # Fetch price
                try:
                    price = item.find_element(By.CSS_SELECTOR, info['price']).text
                except NoSuchElementException:
                    price = "Not found"
                if 'card' in product_name.lower():
                    price_data = {
                        'store': store,
                        'model': search_term,
                        'price': price,
                        'link': product_link,
                        'timestamp': datetime.utcnow()
                    }
                    price_collection.insert_one(price_data)
                    duplicate_add(price_data)
                    break
            
        except NoSuchElementException:
            print("No items found")
        finally:
            driver.quit()
    return results

gpus = gpu_collection.find({})
for i, gpu in enumerate(gpus):
    print(i)
    get_prices(SearchRequest(search_term=gpu['model']))