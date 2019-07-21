import re
import datetime
import os
#import sqlite3
#from fake_useragent import UserAgent
import shutil
#from stem import Signal
#from stem.control import Controller
#import socket
#import socks
import requests
from random import randint, shuffle
from time import sleep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
'''
controller = Controller.from_port(port=9051)
controller.authenticate()

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def renew_tor():
    controller.signal(Signal.NEWNYM)

def showmyip():
    url = "http://www.showmyip.gr/"
    r = requests.Session()
    page = r.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    try:
	    ip_address = soup.find("span",{"class":"ip_address"}).text.strip()
	    print(ip_address)
	except:
		print('Trouble with printing IP address')
    
UA = UserAgent(fallback='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')

hdr = {'User-Agent': "'"+UA.random+"'",
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
'''
def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #hdr)
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
        stamp['raw_text'] = raw_text.replace('\n',' ').strip()
    except:
        stamp['raw_text'] = None
    
    try:
        temp = stamp['title'].split(' ')
        temp2 = stamp['raw_text'].strip().split(' ')
        stamp['year']=temp2[0].strip()
        stamp['country']=temp[0].strip()
    except:
        stamp['year']=None
        stamp['country']=None
    
    try:
        temp = stamp['raw_text'].split('.')
        SG = temp[1]
        grade_cond = temp[2]
        stamp['SG']=SG.replace('.','').replace('SG','').strip()
        stamp['condition']=grade_cond.strip()
    except:
        stamp['year']=None
        stamp['country']=None
        stamp['condition']=None

    try:
        category = html.find_all("span", {"class":"posted_in"})[0].get_text()
        category = category.replace('Categories:','').strip()
        stamp['category'] = category.replace(', Stamps','')
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
'''
def query_for_previous(stamp):
    # CHECKING IF Stamp IN DB
    os.chdir("/Volumes/Stamps/")
    conn1 = sqlite3.connect('Reference_data.db')
    c = conn1.cursor()
    col_nm = 'url'
    col_nm2 = 'raw_text'
    unique = stamp['url']
    unique2 = stamp['raw_text']
    c.execute('SELECT * FROM kentonphil WHERE "{cn}" LIKE "{un}%" AND "{cn2}" LIKE "{un2}%"'.\
                format(cn=col_nm, cn2=col_nm2, un=unique, un2=unique2))
    all_rows = c.fetchall()
    print(all_rows)
    conn1.close()
    price_update=[]
    price_update.append((stamp['url'],
    stamp['raw_text'],
    stamp['scrape_date'], 
    stamp['price'], 
    stamp['currency']))
    
    if len(all_rows) > 0:
        print ("This is in the database already")
        conn1 = sqlite3.connect('Reference_data.db')
        c = conn1.cursor()
        c.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        conn1.commit()
        conn1.close()
        print (" ")
        #url_count(count)
        sleep(randint(10,45))
        pass
    else:
        os.chdir("/Volumes/Stamps/")
        conn2 = sqlite3.connect('Reference_data.db')
        c2 = conn2.cursor()
        c2.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        conn2.commit()
        conn2.close()
    print("Price Updated")

def file_names(stamp):
    file_name = []
    rand_string = "RAND_"+str(randint(0,100000))
    file_name = [rand_string+"-" + str(i) + ".png" for i in range(len(stamp['image_urls']))]
    return(file_name)

def db_update_image_download(stamp):  
    req = requests.Session()
    directory = "/Volumes/Stamps/stamps/kentonphil/" + str(datetime.datetime.today().strftime('%Y-%m-%d')) +"/"
    image_paths = []
    file_name = file_names(stamp)
    image_paths = [directory + file_name[i] for i in range(len(file_name))]
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    for item in range(0,len(file_name)):
        print (stamp['image_urls'][item])
        try:
            imgRequest1=req.get(stamp['image_urls'][item],headers=hdr, timeout=60, stream=True)
        except:
            print ("waiting...")
            sleep(randint(3000,6000))
            print ("...")
            imgRequest1=req.get(stamp['image_urls'][item], headers=hdr, timeout=60, stream=True)
        if imgRequest1.status_code==200:
            with open(file_name[item],'wb') as localFile:
                imgRequest1.raw.decode_content = True
                shutil.copyfileobj(imgRequest1.raw, localFile)
                sleep(randint(18,30))
    stamp['image_paths']=", ".join(image_paths)
    #url_count += len(image_paths)
    database_update =[]

    # PUTTING NEW STAMPS IN DB
    database_update.append((
        stamp['url'],
        stamp['raw_text'],
        stamp['title'],
        stamp['country'],
        stamp['year'],
        stamp['SG'],
        stamp['condition'],
        stamp['category'],
        stamp['sku'],
        stamp['scrape_date'],
        stamp['image_paths']))
    os.chdir("/Volumes/Stamps/")
    conn = sqlite3.connect('Reference_data.db')
    conn.text_factory = str
    cur = conn.cursor()
    cur.executemany("""INSERT INTO kentonphil ('url','raw_text', 'title', 
    'country', 'year','SG', 'condition', 'category','sku','scrape_date','image_paths') 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", database_update)
    conn.commit()
    conn.close()
    print ("all updated")
    print ("++++++++++++")
    sleep(randint(35,100)) 
'''
# start url

start_url = 'https://kentonphilatelics.com/product-category/stamps/'
start_dicts = {'stamps':'https://kentonphilatelics.com/product-category/stamps/',
'covers':'https://kentonphilatelics.com/product-category/covers/',
'varieties':'https://kentonphilatelics.com/product-category/varieties/'}

for key,value in start_dicts.items():
    print (key, value)
selection = input('Make a selection: ')

# loop through all categories
count = 0
#connectTor()
#showmyip()
categories = get_categories(selection)
for category in categories:
    # loop through all subcategories
    subcategories = get_categories(category) 
    for subcategory in subcategories:
        count += 1
        # loop trough every item in current (sub)category
        category_items = get_category_items(subcategory)
        for category_item in category_items:
            # get current item details 
            count+=1
            if count > randint(75,156):
                sleep(randint(500,2000))
                #connectTor()
                #showmyip()
                count = 0
            else:
                pass
            stamp = get_details(category_item)
            #query_for_previous(stamp)
            #db_update_image_download(stamp)
            count += len(file_names(stamp))