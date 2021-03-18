import re
import signal
import sys
import threading
import time
import urllib

import browser_cookie3 as browsercookie
import requests
from bs4 import BeautifulSoup

threads = None

def checklogin(s):
    soup = BeautifulSoup(s.get('https://secure.newegg.com/account/settings').text, 'lxml')
    if soup.find('h2', {'class': 'page-title-second-text'}) is not None and soup.find('h2', {'class': 'page-title-second-text'}).text == 'Account Settings':
        name = soup.find('strong', {'class': 'form-current-value no-margin'}).text
        return (True, name)
    else:
        return (False, None)

def getproductlist():
    f = open('productlist.txt', 'r')
    for product in f:
        if len(product) > 0:
            yield product.strip()
    f.close()

def outofstock(s, product):
    soup = BeautifulSoup(s.get(product).text, 'lxml')
    e = soup.find('div', {'class': 'flags-body has-icon-left fa-exclamation-triangle'})
    e = soup.find('div', {'class': 'flags-body has-icon-left fa-exclamation-triangle'}).span if e is not None else None
    if e is not None and e.text.strip() == 'OUT OF STOCK':
        return True
    return False

def addtocart(s, product, prod_id, user_id):
    payload = {
        'ItemList': [{
            'ItemGroup': 'Single',
            'ItemNumber': prod_id,
            'Quantity': 1,
            'OptionalInfos': None,
            'SaleType': 'Sales'
        }],
        'CustomerNumber': user_id
    }
    resp = s.post('https://www.newegg.com/api/Add2Cart', json=payload).text
    return bool(re.search('"Result":"Success"', resp))

def order(cookie, product, user_id, delay):
    s = requests.Session()
    s.cookies = cookie

    soup = BeautifulSoup(s.get(product).text, 'lxml')
    prod_id = soup.find('ol', {'class': 'breadcrumb'}).find('li', {'class': 'is-current'}).em.text.strip()
    prod_name = soup.title.text[:-13]

    t = threading.currentThread()
    while getattr(t, "running", True):
        if not outofstock(s, product):
            if addtocart(s, product, prod_id, user_id):
                print(f'Successfully added {prod_name} to cart!')
                print(str(threading.activeCount() - 2) + ' products left to order.')
                break
        sleep(delay)
            

def main():
    delay = 1
    if len(sys.argv) > 1:
        try:
            delay = float(sys.argv[1])
        except ValueError:
            print(f'Invalid delay: {sys.argv[1]}')
            return
    print(f'Delay set at {delay} seconds.')

    cookie = browsercookie.chrome(domain_name='.newegg.com')
    s = requests.Session()
    s.cookies = cookie

    cookiedict = requests.utils.dict_from_cookiejar(cookie)
    user_id = urllib.parse.unquote(re.search(r'"sc":"([^"]+)"', urllib.parse.unquote(cookiedict['NV%5FOTHERINFO'])).group(1))
    
    login = checklogin(s)
    if not login[0]:
        print('Not logged in. Please log into your NewEgg account from Google Chrome first.')
        return
    else:
        print(f'Detected NewEgg account name: {login[1]}.')
    
    products = list(getproductlist())
    print(f'Found {len(products)} products to order.')

    threads = []
    for product in products:
        thread = threading.Thread(target=order, args=(cookie, product, user_id, delay))
        thread.running = True
        thread.start()
        threads.append(thread)
    
    try:
        seconds = 0
        while True:
            time.sleep(1)
            seconds += 1
            print (f'Running time: {seconds} seconds. Ctrl+C to stop program.', end='\r')
    except KeyboardInterrupt:
        print('\nQuitting.')
        for thread in threads:
            thread.running = False
            thread.join()

main()
