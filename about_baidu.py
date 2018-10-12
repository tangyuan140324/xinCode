#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/10 15:25
# @Author : HyDady
# @Site : 
# @File : about_baidu.py
# @Software: PyCharm
from urllib import parse
import hashlib
import requests
sk = 'wof1LVcGwjtt7zj6G312KnHnWCtEebGT'
ak = 'l3nrQmIEIQeSYZf2w6KCO4wzzamkwlBN'
key = 'a555954b774b27dbaf7441e3c7a5074b'
def get_urt(address):
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
    queryStr = '/geocoder/v2/?address=%s&output=json&ak=l3nrQmIEIQeSYZf2w6KCO4wzzamkwlBN' % address

    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

    # 在最后直接追加上yoursk
    rawStr = encodedStr + sk#'你的sk'

    # 计算sn
    sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())

    # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")

    return url

def get_json(url):
    res = requests.get(url)
    return_json = res.json()
    return return_json

def use_gaode(x1,y1,x2,y2):
    url = 'https://www.amap.com/service/nav/bus?night=1&' \
          'group=1&pure_walk=1&' \
          'date=2018-10-11&' \
          'time=11-02&type=0&eta=1&' \
          'x1={}&' \
          'y1={}&' \
          'x2={}&' \
          'y2={}'.format(x1,y1,x2,y2)
    res = requests.get(url)
    data = res.json()
    return data
    pass

def gaode_info(keywords,city):
    url = 'https://restapi.amap.com/v3/place/text?key={}&keywords={}&city={}&children=1&offset=20&page=1&extensions=all'.format(key,keywords,city)
    res = requests.get(url)
    info = res.json()
    return info
if __name__=='__main__':
    # or_address = '上海站'
    # de_address = '上海迪士尼'
    # or_url = get_urt(or_address)
    # return_json_or = get_json(or_url)
    # de_url = get_urt(de_address)
    # return_json_de = get_json(de_url)
    # print(return_json_or)
    # '''
    # return_json = {'status': 0, 'result': {'location': {'lng': 121.44296255460806, 'lat': 28.683587738938737}, 'precise': 1, 'confidence': 80, 'comprehension': 100, 'level': '购物'}}
    # x1 = '121.455739'
    # y1 = '31.249563'
    # '''
    # x1 = str(return_json_or['result']['location']['lng'])
    # y1 = str(return_json_or['result']['location']['lat'])
    # x2 = str(return_json_de['result']['location']['lng'])
    # y2 = str(return_json_or['result']['location']['lat'])
    # print(x1,y1,x2,y2)
    # data = use_gaode(x1,y1,x2,y2)
    # print(data)
    print('__________________________________________________________________')
    or_address = '南京南站'
    de_address = '玄武湖'
    city = '南京'
    '''
    获取出发地的经纬度。
    '''
    info_or = gaode_info(or_address,city)
    location_or = info_or['pois'][0]['location']
    location_list_or = location_or.split(',')
    x1 = location_list_or[0]
    y1 = location_list_or[1]
    '''
    获取到达地的经纬度。
    '''
    info_de = gaode_info(de_address,city)
    location_de = info_de['pois'][0]['location']
    location_list_de = location_de.split(',')
    x2 = location_list_de[0]
    y2 = location_list_de[1]
    print(x1,y1,x2,y2)
    data = use_gaode(x1, y1, x2, y2)
    #print(data)
    iwant = data['data']['buslist']  # [0]#['expense']
    taxitime = data['data']['taxitime']
    taxicost = data['data']['taxicost']
    lix = []
    tmp_taxi = {}
    tmp_taxi['taxitime'] = taxitime
    tmp_taxi['taxicost'] = taxicost
    lix.append(tmp_taxi)
    for item in iwant:
        tmp_bus = {}
        tmp_bus['expense'] = item['expense']
        tmp_bus['expensetime'] = item['expensetime']
        tmp_bus['allLength'] = item['allLength']
        tmp_bus['allfootlength'] = item['allfootlength']
        lix.append(tmp_bus)
    print(lix)
    pass