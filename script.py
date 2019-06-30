import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep
from random import randint,shuffle
#from fake_useragent import UserAgent

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except: 
        pass
        
    return html_content

def get_category_items(category_url):
    items = []
    try:
        category_html = get_html(category_url)
        for item in category_html.select('.woocommerce-loop-product__link'):
            items.append(item.get('href'))
    except: 
        pass
    shuffle(items)
    return items

def get_categories(url):
    items = []
    try:
        html = get_html(url)
        category_items = html.find_all('li', {'class': 'product-category'})
        for category_item in category_items:
            item = category_item.find('a').get('href')
            items.append(item)
    except: 
        pass
    shuffle(items)
    return items

def get_details(url):
    
    stamp = {}

    try:
       html = get_html(url)
    except:
       return stamp

    try:
        price_cont = html.find_all("div", {"class":"entry-summary"})[0]
        price = price_cont.find_all("span", {"class":"woocommerce-Price-amount"})[0].get_text()
        price = price.replace(",", "")
        stamp['price'] = price.replace('$','')
    except:
        stamp['price'] = None

    try:
        name = html.find_all("h1", {"class":"product_title"})[0].get_text()
        stamp['title'] = name
    except:
        stamp['title'] = None

    try:
        sku = html.find_all("span", {"class":"sku"})[0].get_text()
        stamp['sku']=sku
    except:
        stamp['sku']=None

    try:
        raw_text = html.find_all("div", {"class":"woocommerce-product-details__short-description"})[0].get_text()
        stamp['raw_text'] = raw_text.replace('\n',' ')
    except:
        stamp['raw_text'] = None

    try:
        category = html.find_all("span", {"class":"posted_in"})[0].get_text()
        category = category.replace('Categories:','').strip()
        stamp['category'] = category
    except:
        stamp['category'] = None

    stamp['currency'] = 'USD'

    # image_urls should be a list
    images = []
    try:
        image_items = html.find_all('div', {'class': 'woocommerce-product-gallery__image'})
        for image_item in image_items:
            img = image_item.find('a').get('href')
            images.append(img)
    except:
        pass

    stamp['image_urls'] = images 

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(22,99))
    return stamp

# start url
start_url = 'https://kentonphilatelics.com/product-category/stamps/'

# loop through all categories
categories = get_categories(start_url)
for category in categories:
    # loop through all subcategories
    subcategories = get_categories(category) 
    for subcategory in subcategories:
        # loop trough every item in current (sub)category
        category_items = get_category_items(subcategory)
        for category_item in category_items:
            # get current item details 
            stamp = get_details(category_item)
         