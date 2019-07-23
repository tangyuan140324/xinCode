#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 上午11:47
# @Author  : dexin.Huang
# @File    : pyspider_companyS.py
import xlrd
from bs4 import BeautifulSoup
from pyspider.libs.base_handler import *
import time

path = '/home/hdx/Desktop/shiyou_info.xlsx'
class Handler(BaseHandler):
    @every(minutes=5 * 24 * 60)
    def on_start(self):
        def xlrd_read_body():
            table = xlrd.open_workbook(path).sheet_by_index(4)
            body_list = []
            body_loop = 1
            while True:
                body_data = {}
                for i in range(table.ncols):
                    body_data[table.cell(0, i).value] = table.cell(body_loop, i).value
                body_list.append(body_data)
                body_loop += 1
                if body_loop >= table.nrows:  # 大于表格的总行数就退出循环
                    break
            return body_list
        home_page_list = xlrd_read_body
        # for i, item in enumerate(home_page_list):
        #     if home_page_list[i]['数据来源'] is not '':
        #         self.crawl(item['数据来源'], callback=getattr(self, 'func' + str(int(item['序号'])))
        for item in home_page_list:
            if item['数据来源'] is not '':
                save = {'url': item['数据来源']}
                self.crawl(item['数据来源'], save = save, callback=getattr(self, 'func_'+ str(int(item['序号']))))


    @config(age=24 * 60 * 60)
    def company_henyi(self, response):
        home_page = 'http://www.hengyi.com/'
        infos = BeautifulSoup(response.text, 'lxml')
        url_remains = infos.find('div', class_='quickentr').findAll('li')
        url_list = []
        for item in url_remains:
            dic = {}
            dic['url'] = home_page + item.a['href']
            dic['type'] = 'company'
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "浙江恒逸集团有限公司"
            url_list.append(dic)
        next_page = 'http://www.phosphatechina.com/'
        self.crawl(next_page, callback=self.company_phosphatechina)
        return url_list

    @config(age=24 * 60 * 60)
    def company_phosphatechina(self, response):
        home_page = 'http://www.phosphatechina.com/'
        infos = BeautifulSoup(response.content, 'lxml')
        url_remains = infos.findAll('li', class_='menu-item')
        url_list = []
        for item in url_remains:
            dic = {}
            dic['url'] = home_page + item.a['href']
            dic['type'] = 'company'
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "江阴澄星实业集团有限公司"
            url_list.append(dic)
        next_page = 'http://www.lihuayi.com/'
        self.crawl(next_page, callback=self.company_lihuayi)
        return url_list

    @config(age=24 * 60 * 60)
    def company_lihuayi(self, response):
        home_page = 'http://www.lihuayi.com/'
        infos = BeautifulSoup(response.content, 'lxml')
        b = infos.findAll('ul')
        url_list = []
        for item in b:
            sb = item.findAll('li')
            for x in sb:
                dic = {}
                dic['url'] = home_page + item.a['href']
                dic['type'] = 'company'
                dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
                dic["source"] = "利华益集团股份有限公司"
                url_list.append(dic)
        next_page = 'http://www.dmsh.com.cn/'
        self.crawl(next_page, callback=self.company_dmsh)
        return url_list

    @config(age=24 * 60 * 60)
    def company_dmsh(self, response):
        home_page = 'http://www.dmsh.com.cn/'
        infos = BeautifulSoup(response.content, 'lxml')
        url_remains = infos.findAll('ul', class_='list-none')[1].findAll('dd')
        url_list = []
        for item in url_remains:
            dic = {}
            dic['url'] = home_page + item.a['href']
            dic['type'] = 'company'
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "山东东明石化集团有限公司"
            url_list.append(dic)
        next_page = 'http://www.rong-sheng.com/page/html/frame.php'
        self.crawl(next_page, callback=self.company_rongsheng)
        return url_list

    @config(age=24 * 60 * 60)
    def company_rongsheng(self, response):
        home_page = 'http://www.rong-sheng.com/page/html/frame.php'
        infos = BeautifulSoup(response.content, 'lxml')
        url_remains = infos.find('div', class_='maxmenu').findAll('a')
        url_list = []
        for item in url_remains:
            dic = {}
            dic['url'] = home_page + item['href']
            dic['type'] = 'company'
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "浙江荣盛控股集团责任有限公司"
            url_list.append(dic)
        next_page = 'http://www.pmjt.com.cn/'
        self.crawl(next_page, callback=self.company_pmjt)
        return url_list
    @config(age=24 * 60 * 60)
    def company_pmjt(self, response):
        home_page = 'http://www.pmjt.com.cn/'
        infos = BeautifulSoup(response.content, 'lxml')
        url_remains = infos.find('div', class_='menu').findAll('a')
        url_list = []
        for item in url_remains:
            dic = {}
            dic['url'] = home_page + item['href']
            dic['type'] = 'company'
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "中国平煤神马能源化工集团有限责任公司"
            url_list.append(dic)
        next_page = 'http://www.pmjt.com.cn/'
        self.crawl(next_page, callback=self.company_pmjt)

    @config(age=24 * 60 * 60)
    def func_3(self, response):
        infos = BeautifulSoup(response.content, 'lxml')
        url_remains = infos.find('div', class_='nav').findAll('li')
        home_page = response.save['url']
        url_list = []
        for item in url_remains:
            dic = {}
            dic['url'] = home_page + item.a['href']
            dic['type'] = 'company'
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "中国海洋石油集团有限公司"
            url_list.append(dic)
        return url_list

    @config(age=24 * 60 * 60)
    def func_5(self, response):
        infos = BeautifulSoup(response.content, 'lxml')
        url_remains = infos.find('div', id='nav').findAll('li')
        url_list = []
        for item in url_remains:
            dic = {}
            dic['url'] = 'http://www.chemchina.com.cn' + item.a['href']
            dic['type'] = 'company'
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "中国化工集团公司"
            url_list.append(dic)

        return url_list


    @config(age=24 * 60 * 60)
    def func_6(self, response):
        home_page = response.save['url']
        infos = BeautifulSoup(response.content, 'lxml')
        url_remains = infos.find('table', id='t1_2_').findAll('td', valign='middle')
        url_list = []
        for item in url_remains:
            dic = {}
            dic['url'] = home_page + item.a['href']
            dic['type'] = 'company'
            dic["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            dic["source"] = "陕西延长石油（集团）有限责任公司"
            url_list.append(dic)
        return url_list