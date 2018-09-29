# -*- coding: utf-8 -*-
import base64
import hashlib
import random
from urllib.parse import urljoin
import time
from bs4 import BeautifulSoup
import requests
from redis_update import oPut_proxy_redis
from math import floor
import re

proxy_list_out = oPut_proxy_redis()
def judgement_ch(**kwargs):
    if kwargs['isTmall']:
        return kwargs['detail_url']


def parser(item,currentUrl,response):
        try:
            view_sales = item['view_sales']
        except KeyError:
            view_sales = "-1pay"
        detail_url = urljoin(currentUrl, item['detail_url'])
        uz_id = hashlib.md5((str(item['nid'])+str(time.time())).encode('utf-8')).hexdigest()
        temple = {
            'title': BeautifulSoup(item['title'], 'lxml').get_text().strip(),
            'view_price': item['view_price'],
            'view_sales': view_sales,
            'view_fee': False if float(item['view_fee']) else True,
            'isTmall': True if item['shopcard']['isTmall'] else False,
            'nid': item['nid'],
            'source_nid': item['nid'],
            'detail_url': detail_url,
            'crawlDate': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'productType': response.save['keyword'],
            'item_loc': item['item_loc'],
            'nick': item['nick'],
            'user_id': item['user_id'],
            'dateType':"list",
            '_meta':{ 'store': 'mongodb' },
            'uz_id':uz_id
        }
        return temple

def fuck_taobao(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    html = requests.get(url,headers,proxies = random.choice(proxy_list_out)).text
    if 'listItem' in html:
        #print(html)
        return True
    else:
        return False

def binarySearch(url, page1=1, page2=100):
    global rightPage
    #print("Now testing %i,%i" %(page1,page2))
    halfPage = floor((page1 + page2)/2)
    url = re.sub(r'page=([0-9]*)', 'page='+str(halfPage), url)
    isRight = fuck_taobao(url)
    if isRight == True:
        page1 = halfPage
        page2 = page2
    else:
        page1 = page1
        page2 = halfPage

    nextHalfPage = floor((page1 + page2)/2)
    if nextHalfPage != halfPage:
        binarySearch(url, page1,page2)
    else:
        url = re.sub(r'page=([0-9]*)', 'page='+str(page2), url)
        isRight = fuck_taobao(url)
        if isRight == True:
            rightPage = page2
        else:
            rightPage = page1
    return rightPage

def dowloadPic(type,response):
    photo_list = []
    html = response.text
    if type == 'taobao':
        location = re.findall(r'img data-src="(.*?)" /></a>', html, re.S)
    elif type == 'tmall':
        location= re.findall(r'img src="(.*?)" /></a>',html,re.S)
    else:
        return "type error"
    for i in range(len(location)):
        if "http" in location[i]:
            url_new = location[i]
        else:
            url_new = 'https:' + location[i]
        photo = requests.get(url_new)
        basecode = base64.b64encode(photo.content)
        num = str(basecode, 'utf-8')
        photo_list.append(num)
        # with open(nid + str(i) + ".jpg", 'wb') as f:
        #     f.write(photo.content)
    return photo_list
if __name__ =="__main__":
    pass













