#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/17 下午2:54
# @Author  : dexin.Huang
# @File    : puspider_compangy_hengyi.py


from bs4 import BeautifulSoup
from pyspider.libs.base_handler import *
import re
import time


class Handler(BaseHandler):
    @every(minutes=5 * 24 * 60)
    def on_start(self):
        home_page = 'http://www.hengyi.com/'
        self.crawl(home_page, callback=self.company_remains)

    @config(age=24 * 60 * 60)
    def company_remains(self, response):
        home_page = 'http://www.hengyi.com/'
        infos = BeautifulSoup(response.text, 'lxml')
        url_remains = infos.find('div', class_='quickentr').findAll('li')
        url_list = []
        for item in url_remains:
            dic = {}
            dic['lable_url'] = home_page + item.a['href']
            dic['lable'] = item.a.getText().replace('  ', '')
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "浙江恒逸集团有限公司"
            url_list.append(dic)
        return url_list
