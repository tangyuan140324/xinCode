#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 下午4:34
# @Author  : dexin.Huang
# @File    : pyspider_compang_phosphatechina.py


from bs4 import BeautifulSoup
from pyspider.libs.base_handler import *
import re
import time


class Handler(BaseHandler):
    @every(minutes=5 * 24 * 60)
    def on_start(self):
        home_page = 'http://www.phosphatechina.com/'
        self.crawl(home_page, callback=self.company_remains)

    @config(age=24 * 60 * 60)
    def company_remains(self, response):
        home_page = 'http://www.phosphatechina.com/'
        infos = BeautifulSoup(response.content, 'lxml')
        url_remains = infos.findAll('li', class_='menu-item')
        url_list = []
        for item in url_remains:
            dic = {}
            dic['lable_url'] = home_page + item.a['href']
            dic['lable'] = item.a.getText().replace('  ', '')
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "江阴澄星实业集团有限公司"
            url_list.append(dic)
        return url_list
