# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: jd

from bs4 import BeautifulSoup
from pyspider.libs.base_handler import *
import re
from Api import *

####################


keywordsConfigPath = '/web/spider/config/keywords.conf'
keywordsDonePath = '/web/spider/log/keywordsDone.log'
wr = configparser.ConfigParser()
wr.read("/web/spider/config/host.conf")

host = wr.get('redis', 'redis_host')
port = wr.get('redis', 'redis_port')

headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }

class Handler(BaseHandler):
    @every(minutes=5 * 24 * 60)
    def on_start(self):
        def get_keywords(n=1):
            # Read config file for keyword and page_count.
            with open(keywordsConfigPath, 'r') as f:
                keywords = f.read().split(",")
                if keywords == ['']:
                    print("All keywords cralwed.")
                    return
            keyword = keywords[0:n]
            b = ",".join(keyword[0:n])
            a = ",".join(keywords[n:])
            with open(keywordsConfigPath, 'w') as fp:
                fp.write(a)
            with open(keywordsDonePath, 'a') as g:
                if keywords != ['']:
                    g.write(',' + b)
            return keyword
        li = get_keywords()
        for keyword in li:
            url = "https://search.jd.com/Search?enc=utf-8&" + keyword
            save = {'keyword': keyword}
            self.crawl(url, callback=self.listpage, save=save, validate_cert=False)

    @config(age=24 * 60 * 60)
    def listpage(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        page = str(soup.find('div', class_='f-pager'))
        try:
            totalPage = re.findall(r'<i>([0-9]*)</i>', page, re.S)[0]
        except:
            totalPage = 100
        #save = {'keyword':response.save['keyword']}
        keyword = wq = response.save['keyword']
        for x in range(1, int(totalPage)):
            url = "https://search.jd.com/Search?keyword={}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={}" \
                  "page={}&s=56&click=0".format(keyword, wq, str(x))
            self.crawl(url, callback=self.firstPageBottomHalf,validate_cert=False, headers=headers)

    @config(age=24 * 60 * 60)
    def firstPageBottomHalf(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        data = []
        lis = soup.find_all("li", class_='gl-item')
        for li in lis:
            temp = {}
            if li.find("a")['href']:
                temp['p_img'] = "https"+li.find("a")['href']
            if li.find('a')['title']:
                temp['title'] = li.find('a')['title']
            if li.find('div', {"class": "p-price"}).getText():
                temp['price'] = li.find('div', {"class": "p-price"}).getText().strip()
            if li.find('div', {"class": "p-shop"}).getText():
                temp['shopName'] = li.find('div', {"class": "p-shop"}).getText().strip()
            try:
                fid_url = li.find('a', {"class": "curr-shop"})
                temp['url'] = 'https:' + re.findall(r'href="(.*?)"', str(fid_url), re.S)[0]
            except:
                temp['url'] = None
            if li.find('div', {"class": "p-commit"}).getText():
                temp['commit'] = li.find('div', {"class": "p-commit"}).getText().strip()
            if li.get("data-pid"):
                temp['data_pid'] = li.get("data-pid")
            data.append(temp)
            shop_url = temp['url']
            self.crawl(shop_url, callback=self.shopList, validate_cert=False, headers=headers)
        return data

    def shopList(self, response):
        html = response.text