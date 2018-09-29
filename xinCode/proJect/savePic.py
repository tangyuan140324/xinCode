#!/usr/bin/env python
# coding:utf-8
import configparser
import json
import re
import requests
import time

from dataToMongo import getConsumer


cf = configparser.ConfigParser()
cf.read("/web/spider/config/host.conf")

kafka_host = cf.get('kafka','kafka_host')

kafka_port = int(cf.get('kafka','kafka_port'))
savePath = '/data01/picture/'

def dowloadPic(loc,response,nid):
    html = response.text
    title = re.findall(r'<title>(.*?)</title>', html, re.S)[0]
    if '/' in title:
        title = title.replace('/','--')
    if loc == 'taobao':
            location = re.findall(r'img data-src="(.*?)" /></a>', html, re.S)
    elif loc == 'tmall':
        location= re.findall(r'img src="(.*?)" /></a>',html,re.S)
    else:
        return "type error"
    for i in range(len(location)):
        tep = location[i].split('.jpg')[0]
        tep_c = tep + '.jpg'
        if tep_c[0:2] != '//':
            url_new = tep_c
        else:
            url_new = 'https:' + tep_c
        print(url_new)
        photo = requests.get(url_new)
        with open(savePath + title +"_"+ str(nid) + "_" + str(i) + ".jpg", 'wb') as f:
            f.write(photo.content)

def picFunc():
    consumer = getConsumer(kafka_host, kafka_port, b'downimg', False, kafka_host)
    for msg in consumer:
        consumer.commit_offsets()  #标记offset
        offset = msg.offset
        if msg is not None :
            data =json.loads(msg.value,encoding="utf-8")
            img_urls = data['img_urls']
            title = data['title']
            nid = data['nid']
            for i in range(len(img_urls)):
                with requests.get(img_urls[i], stream=True) as r:
                    with open(savePath + title + "_" + str(nid) + "_" + str(i) + ".jpg", 'wb') as f:
                        f.write(r.content)


if __name__ == '__main__':
    pass
