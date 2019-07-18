#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/17 上午10:46
# @Author  : dexin.Huang
# @File    : sinopec_html.py

import requests
from bs4 import BeautifulSoup
url = 'http://www.phosphatechina.com/'

response = requests.get(url)
#response.encoding = 'gzip'
infos = BeautifulSoup(response.content, 'lxml')
url_remains = infos.findAll('li', class_='menu-item')
# print(url_remains)
# print(len(url_remains))
url_list = []
for item in url_remains:
    dic = {}
    dic['lable_url'] = url + item.a['href']
    dic['lable'] = item.a.getText().replace('  ', '')
    url_list.append(dic)
print(url_list)
