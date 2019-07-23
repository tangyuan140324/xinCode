#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 下午2:19
# @Author  : dexin.Huang
# @File    : pyspider_zjhp_2019_07_11.py




import hashlib
import random
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pyspider.libs.base_handler import *
import re
import time
import json
savePath = '/data01/html/zjssthjt/'

class Handler(BaseHandler):
    @every(minutes=5 * 24 * 60)
    def on_start(self):
        beg_url = 'http://www.zjepb.gov.cn/module/xxgk/search.jsp?divid=div1201347&infotypeId=A001AD001A001A001' \
                  '&jdid=1756&area=002482429&sortfield='
        self.crawl(beg_url, callback=self.zjhp_spiderUrls)

    @config(age=24 * 60 * 60)
    def zjhp_spiderUrls(self, response):
        total_page = re.findall(r'&nbsp;&nbsp;共(.*?)页&nbsp;', response.text, re.S)[0]
        url_list = []
        for i in range(1, int(total_page)+1):
            url = 'http://www.zjepb.gov.cn/module/xxgk/search.jsp?' \
                  'infotypeId=A001AD001&jdid=1756&area=&divid=div1201347&vc_title=&vc_number=&sortfield=,compaltedate:0&currpage={}' \
                  '&vc_filenumber=&vc_all=&texttype=&fbtime=&texttype=&fbtime=&vc_all=&vc_filenumber=&' \
                  'vc_title=&vc_number=&currpage={}&sortfield=,compaltedate:0'.format(str(i), str(i))
            url_list.append(url)
        self.crawl(url_list, timeout=10, callback=self.zjhp_condition_remains)


    @config(age=24 * 60 * 60)
    def zjhp_condition_remains(self, response):
        html_detail_tbody = BeautifulSoup(response.text, 'lxml')
        infos_list = []
        tbodys_one = html_detail_tbody.findAll("tr", class_='tr_main_value_even')
        tbodys_two = html_detail_tbody.findAll("tr", class_='tr_main_value_odd')
        for infos in tbodys_one + tbodys_two:
            html_info = {}
            if infos.a is not None:
                html_info["url"] = infos.a['href']
                html_info["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
                html_info["source"] = "浙江省生态环境厅"
                infos_list.append(html_info)
        return infos_list
        # for sub_url in infos_list:
        #     save = {'sub_url': sub_url}







    #         self.crawl(sub_url, save=save, callback=self.detail_zjhp_datainfo)
    #
    # @config(age=24 * 60 * 60)
    # def detail_zjhp_datainfo(self, response):
    #     # html_name = response.save['sub_url']
    #     # with open(savePath+html_name, 'wb') as f:
    #     #     f.write(response.content)
    #     data_info = {}
    #     data_info['sub_url'] = response.save['sub_url']
    #     oBject = BeautifulSoup(response.text, 'lxml')
    #     title = oBject.find('div', class_='mainContainer;').findAll('tr')[0].getText()
    #     data_info['标题'] = title
    #
    #     x = oBject.find("div", class_='mainContainer;').findAll('a')
    #     pdf_url_list = []
    #     pdf_name_list = []
    #     for i in range(len(x)):
    #         j = oBject.find("div", class_='mainContainer;').findAll('a')[i]['href']
    #         k = x[i].getText()
    #         pdf_name_list.append(k)
    #         try:
    #             url_part = re.findall(r"&filename=(.*?).pdf", j, re.S)[0]
    #             if '/module/download/downfile.jsp?' in j:
    #                 pdf_url_list.append('http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files'
    #                                     '/jcms1/web1756/site/attach/-1/{}.pdf'.format(url_part))
    #             else:
    #                 pdf_url_list.append(url_part)
    #         except IndexError:
    #             url_part = 'http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web1756/site{}'.format(j)
    #             pdf_url_list.append(url_part)
    #     data_info['pdf_name_list'] = pdf_name_list
    #     data_info['pdf_url_list'] = pdf_url_list
    #     return data_info
