#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 下午6:14
# @Author  : dexin.Huang
# @File    : demo1.py
import re
import requests
from bs4 import BeautifulSoup

#url = 'http://www.zjepb.gov.cn/art/2018/11/21/art_1201950_25491698.html'
url = 'http://www.zjepb.gov.cn/col/col1201347/index.html'
response = requests.get(url)
response.encoding = "utf-8"

# data_info = {}
# oBject = BeautifulSoup(res.text, 'lxml')
# title = oBject.find('div', class_='mainContainer;').findAll('tr')[0].getText()
# try:
#     part_one = oBject.find("table", class_='MsoNormalTable').findAll('tr')
#     if len(part_one) >= 2:
#         str1 = part_one[0].getText().replace('\n\n\n', '|').replace('\n', '').split('|')
#         for i in range(1, len(part_one)):
#             str_i = part_one[i].getText().replace('\n\n\n', '|').replace('\n', '').split('|')
#             data_info = dict(zip(str1, str_i))
#     elif len(part_one) < 2:
#         pass
#     else:
#         pass
# except AttributeError:
#     part_one = oBject.find("div", id='zoom').findAll('tr')
#     if len(part_one) >= 2:
#         str1 = [item.getText() for item in part_one[0].findAll('th')]
#         for i in range(1, len(part_one)):
#             str_i = [item.getText().replace('\xa0', '').replace('\xa0351', '') for item in part_one[i].findAll('td')]
#             data_info = dict(zip(str1, str_i))
#     elif len(part_one) < 2:
#         pass
#     else:
#         pass
# data_info['标题'] = title
#
# try:
#     part_two = oBject.find("div", class_='TRS_PreAppend').findAll('p', class_="MsoNormal")
#     data_info['公告时间'] = part_two[15].getText().split('：')[1]
#     data_info['联系人'] = part_two[16].getText().split('：')[1]
#     data_info['联系电话'] = part_two[17].getText().split('  ')[0].split('：')[1]
#     data_info['传真'] = part_two[17].getText().split('  ')[1].split('：')[1]
#     data_info['通讯地址'] = part_two[18].getText().split('：')[1]
#     data_info['Tips'] = part_two[19].getText()
# except AttributeError:
#     li = []
#     part_two = [li.append(item.replace('\xa0\xa0\xa0\xa0\xa0\xa0\xa0', '')) for item in oBject.find("div", id='	')
#         .getText().split('\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0')]
#     str3_list = ''.join(li).split('\n')
#     data_info['公告时间'] = str3_list[-5].split('：')[1]
#     data_info['联系人'] = str3_list[-4].split('：')[1]
#     data_info['联系电话'] = str3_list[-3].split('\xa0\xa0\xa0\xa0\xa0\xa0')[0].split('：')[1]
#     data_info['传真'] = str3_list[-3].split('\xa0\xa0\xa0\xa0\xa0\xa0')[1].split('：')[1]
#     data_info['通讯地址'] = str3_list[-2].split('：')[1]
#     data_info['Tips'] = str3_list[-1]
# # ========================================================================================
# x = oBject.find("div", class_='mainContainer;').findAll('a')
# pdf_url_list = []
# pdf_name_list = []
# for i in range(len(x)):
#     j = oBject.find("div", class_='mainContainer;').findAll('a')[i]['href']
#     k = x[i].getText()
#     url_part = re.findall(r"&filename=(.*?).pdf", j, re.S)[0]
#     if '/module/download/downfile.jsp?' in j:
#         pdf_name_list .append(k)
#         pdf_url_list.append('http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files'
#                             '/jcms1/web1756/site/attach/-1/{}.pdf'.format(url_part))
#     else:
#         pdf_url_list.append(url_part)
# data_info['pdf_name_list'] = pdf_name_list
# data_info['pdf_url_list'] = pdf_url_list

data_info = {}
oBject = BeautifulSoup(response.text, 'lxml')
title = oBject.find('div', class_='mainContainer;').findAll('tr')[0].getText()
data_info['标题'] = title

x = oBject.find("div", class_='mainContainer;').findAll('a')
print(x)
pdf_url_list = []
pdf_name_list = []
for i in range(len(x)):
    j = oBject.find("div", class_='mainContainer;').findAll('a')[i]['href']
    k = x[i].getText()
    pdf_name_list.append(k)
    try:
        url_part = re.findall(r"&filename=(.*?).pdf", j, re.S)[0]
        if '/module/download/downfile.jsp?' in j:
            pdf_url_list.append('http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files'
                                '/jcms1/web1756/site/attach/-1/{}.pdf'.format(url_part))
        else:
            pdf_url_list.append(url_part)
    except IndexError:
        url_part = 'http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web1756/site{}'.format(j)
        pdf_url_list.append(url_part)
data_info['pdf_name_list'] = pdf_name_list
data_info['pdf_url_list'] = pdf_url_list


print(data_info)

# http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web1756/site/attach/-1/1811211346356196857.pdf
#/attach/-1/1811211346356196857.pdf

