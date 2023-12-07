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
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio


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
    },
    'bestbuy': {
        'product': 'li.sku-item',
        'name': 'h4.sku-title',
        'price': 'div.priceView-hero-price span',
        'link': 'a.image-link',
        'image': 'a.image-link img',
        'base_url': 'https://www.bestbuy.com/site/searchpage.jsp?st=',
        'separator': '+'
    },
    'walmart': {
        'product': 'div.mb0.ph1.pa0-xl.bb.b--near-white.w-25.pb1-xl',
        'name': 'span[data-automation-id="product-title"]',
        'price': 'div[data-automation-id="product-price"]',
        'link': 'a[href]',
        'image': 'img[data-testid="productTileImage"]',
        'base_url': 'https://www.walmart.com/search?q=',
        'separator': '%20'
    },
    'newegg': {
        'product': 'div.item-cell',
        'name': 'a.item-title',
        'price': 'li.price-current',
        'link': 'a.item-title',
        'image': 'a.item-img img',
        'base_url': 'https://www.newegg.com/p/pl?d=',
        'separator': '+'
    },
    'ebay': {
        'product': 'div.s-item__wrapper',
        'name': 'div.s-item__title span',
        'price': 'span.s-item__price',
        'link': 'a.s-item__link',
        'image': 'div.s-item__image-wrapper img',
        'base_url': 'https://www.ebay.com/sch/i.html?_nkw=',
        'separator': '+'
    }
}
async def process_store(store, website_info, search_term, keywords, app):
    print("Searching " + store)
    info = website_info[store]
    driver = create_firefox_driver_with_authenticated_proxy()

    search_term = search_term.replace(' ', info['separator'])
    if store == 'ebay':
        search_term += '&_sacat=0'
    print(info['base_url'] + search_term)
    driver.get(info['base_url'] + search_term)
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
            if 'card' in product_name.lower() and all(keyword in product_name.lower() for keyword in keywords):
                price_data = {
                    'store': store,
                    'product_name': product_name,
                    'product_price': price,
                    'product_link': product_link,
                    'timestamp': datetime.utcnow()
                } 
                return price_data
        
    except NoSuchElementException:
        print("No items found")
    finally:
        driver.quit()

app = FastAPI()


origins = [
    "http://localhost:3000",  # React app origin
    # Add other origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient("mongodb://34.125.160.112/gpuzone")
    app.mongodb = app.mongodb_client["gpuzone"]  # Replace with your database name

@app.post("/prices")
async def get_prices(request_body: SearchRequest):
    search_term = request_body.search_term
    keywords = search_term.split(' ')
    keywords = [keyword.lower() for keyword in keywords]
    print(keywords)
    # # Asynchronously gather results from process_store
    # loop = asyncio.get_running_loop()
    # with ThreadPoolExecutor() as executor:
    #     tasks = [loop.run_in_executor(executor, process_store, store, website_info, search_term, keywords, app) for store in website_info.keys()]
    #     results = await asyncio.gather(*tasks)
    
    # # Process and return results
    # processed_results = [item for item in results if item]  # Filter out None or empty results if needed
    # for res in processed_results:
    #     print(res)
    #     # await app.mongodb["prices"].insert_one(res)
    #     res.pop('_id')

    # return processed_results

    results = []
    for store in website_info.keys():
        print("Searching " + store)
        info = website_info[store]
        driver = create_firefox_driver_with_authenticated_proxy()

        search_term = search_term.replace(' ', info['separator'])
        if store == 'ebay':
            search_term += '&_sacat=0'
        print(info['base_url'] + search_term)
        driver.get(info['base_url'] + search_term)
        try:
            # Locate all item cells
            item_cells = driver.find_elements(By.CSS_SELECTOR, info['product'])
            for item in item_cells:
                # Fetch product name
                try:
                    product_name = item.find_element(By.CSS_SELECTOR, info['name']).text
                except NoSuchElementException:
                    product_name = "Not found"
                # Fetch image URL
                try:
                    product_image_url = item.find_element(By.CSS_SELECTOR, info['image']).get_attribute('src')
                except NoSuchElementException:
                    product_image_url = "Not found"
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
                if 'card' in product_name.lower() and all(keyword in product_name.lower() for keyword in keywords):
                    price_data = {
                        'store': store,
                        'product_name': product_name,
                        'product_price': price,
                        'product_link': product_link,
                        'product_image_url': product_image_url,
                        'timestamp': datetime.utcnow()
                    } 
                    price_data.pop('_id', None)
                    results.append(price_data)
                    await app.mongodb["prices"].insert_one(price_data)
                    break
            
        except NoSuchElementException:
            print("No items found")
        finally:
            driver.quit()
    print(results)
    for item in results:
        item.pop('_id', None)
    return results

@app.get("/gpus")
async def read_gpus(page: int = 1, page_size: int = 9):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be positive")

    skip = (page - 1) * page_size
    items = await app.mongodb["gpu"].find({}, {'_id': 0}).skip(skip).limit(page_size).to_list(length=page_size)
    return items

@app.get("/gpu_count")
async def read_gpus():
    items = await app.mongodb["gpu"].count_documents({})
    return items

@app.post("/last_month_prices")
async def read_last_month_prices(requestBody: SearchRequest):
    model = requestBody.search_term
    last_month = datetime.utcnow() - timedelta(days=30)
    items = await app.mongodb["price"].find({'timestamp': {'$gte': last_month}, 'model': model}, {'_id': 0, 'store': 0, 'link': 0, 'model': 0}).to_list(length=1000000)
    return items