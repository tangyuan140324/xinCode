#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 下午6:14
# @Author  : dexin.Huang
# @File    : demo1.py
import configparser
import json

# cf = configparser.ConfigParser()
#
# data = json.loads(cf.read("/web/spider/config/config.json"))
# print(data)
# mysql_table_pdf_download = cf.get('Mysql', 'mysql_table_pdf_download')
# mysql_table_html_download = cf.get('Mysql', 'mysql_table_html_download')


with open("/web/spider/config/config.test.json", 'r') as f:
    data = json.loads(f.read())
    mysql_table_pdf_download = data['result_worker']['result_settings']['mysql_table_pdf_download']
    print(mysql_table_pdf_download)
    print(type(mysql_table_pdf_download))