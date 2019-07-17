#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 下午5:35
# @Author  : dexin.Huang
# @File    : demo2.py

import os
savePath = '/data01/pdf/'


import requests


for i in range(1,26):
    url = 'http://www.zjepb.gov.cn/module/xxgk/search.jsp?' \
          'infotypeId=A001AD001&jdid=1756&area=&divid=div1201347&vc_title=&vc_number=&sortfield=,compaltedate:0&currpage={}' \
          '&vc_filenumber=&vc_all=&texttype=&fbtime=&texttype=&fbtime=&vc_all=&vc_filenumber=&' \
          'vc_title=&vc_number=&currpage={}&sortfield=,compaltedate:0'.format(str(i), str(i))
    res = requests.get(url)

