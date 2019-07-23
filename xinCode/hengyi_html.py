#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/17 上午10:46
# @Author  : dexin.Huang
# @File    : sinopec_html.py
import operator
import time
from functools import reduce

import requests
from bs4 import BeautifulSoup
home_page = 'http://www.cnpc.com.cn/cnpc/index.shtml'

response = requests.get(home_page)
#response.encoding = 'gzip'
infos = BeautifulSoup(response.content, 'lxml')
url_remains = infos.find('div', class_='mainNav').findAll('a')
# print(url_remains)
# exit()
url_list = []
for item in url_remains:
    dic = {}
    # if 'http://www.cnpc.com.cn' or 'http://csr.cnpc.com.cn' in item['href']:
    #     dic['url'] = item['href']
    # elif 'http://news.cnpc.com.cn' in item['href']:
    #     dic['url'] = item['href']
    # else:
    #     dic['url'] = 'http://www.cnpc.com.cn' + item['href'].replace('../..', '')
    dic['url'] = item['href']
    dic['type'] = 'company'
    dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    dic["source"] = "中国海洋石油集团有限公司"
    dic['lable'] = item.getText()
    url_list.append(dic)

print(url_list)

