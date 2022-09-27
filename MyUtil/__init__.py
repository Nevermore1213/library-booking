__author__ = "define9"
__version__ = "0.0.1"

import requests, json
    
def down2File(filename, content):
    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(content)

def saveCookie(filename, cookies):
    cookie_dict = requests.utils.dict_from_cookiejar(cookies)
    with open(filename, 'w+', encoding='utf-8') as f:
        json.dump(cookie_dict, f)
        
def readCookie(filename):
    cookie_dict = {}
    with open(filename, 'r', encoding='utf-8') as f:
        cookie_dict = json.load(f)
    return requests.utils.cookiejar_from_dict(cookie_dict)
    
def fmt02(num):
    return "{:02d}".format(num)