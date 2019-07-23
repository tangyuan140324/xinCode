#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 下午2:20
# @Author  : dexin.Huang
# @File    : zjhp_part.py


import re
import requests
from bs4 import BeautifulSoup


beg_url = 'http://www.zjepb.gov.cn/module/xxgk/search.jsp?divid=div1201347&infotypeId=A001AD001A001A001' \
          '&jdid=1756&area=002482429&sortfield='
res = requests.get(beg_url)
res.encoding = 'utf-8'
html_content = res.text
# print(html_content)
# exit()
html_detail_tbody = BeautifulSoup(html_content, 'lxml')
infos_list = []
tbodys_one = html_detail_tbody.findAll("tr", class_='tr_main_value_even')
tbodys_two = html_detail_tbody.findAll("tr", class_='tr_main_value_odd')
for infos in tbodys_one:
    dic = {}
    dic['date'] = infos.find("td", align='center').getText()
    if infos.a is not None:
        dic["detail_url"] = infos.a['href']
        dic["detail_title"] = infos.a['title']
    infos_list.append(dic)
for infos in tbodys_two:
    dic = {}
    dic['date'] = infos.find("td", align='center').getText()
    if infos.a is not None:
        dic["detail_url"] = infos.a['href']
        dic["detail_title"] = infos.a['title']
    infos_list.append(dic)
print(infos_list)

total_page = re.findall(r'&nbsp;&nbsp;共(.*?)页&nbsp;', html_content, re.S)[0]
print(total_page)



