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
            table = xlrd.open_workbook(path).sheet_by_index(5)
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
        home_page_list = xlrd_read_body()
        # for i, item in enumerate(home_page_list):
        #     if home_page_list[i]['数据来源'] is not '':
        #         self.crawl(item['数据来源'], callback=getattr(self, 'func' + str(int(item['序号'])))
        for item in home_page_list:
            if item['数据来源'] is not '':
                save = {'url': item['数据来源']}
                self.crawl(item['数据来源'], save=save, callback=getattr(self, 'func_'+ str(int(item['序号']))))


    @config(age=24 * 60 * 60)
    def func_1(self, response):
        home_page = response.save['url']
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
        return url_list

    @config(age=24 * 60 * 60)
    def func_2(self, response):
        home_page = response.save['url']
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
        return url_list

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
    def func_4(self, response):
        home_page = response.save['url']
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

    @config(age=24 * 60 * 60)
    def func_7(self, response):
        home_page = response.save['url']
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
        return url_list

    @config(age=24 * 60 * 60)
    def func_8(self, response):
        home_page = response.save['url']
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
        return url_list

    @config(age=24 * 60 * 60)
    def func_9(self, response):
        home_page = response.save['url']
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
        return url_list

