#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import random

import requests
import time
from bs4 import BeautifulSoup

headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }




def get_ip_url_kuaidaili():
    '''
    创建一个随机的url

    '''
    beg_url = "https://www.kuaidaili.com/free/inha/"
    url_li = []
    for x in range(1,10):
        url = beg_url + str(x) + "/"
        url_li.append(url)
    print(url_li)
    return url_li

def get_ip_list_kuaidaili(url_li, headers):
    '''
     在随机的url拿到当页的ip_proies.

    '''
    ip_list = []
    for url in url_li:
        web_data = requests.get(url, headers=headers)
        time.sleep(1)
        soup = BeautifulSoup(web_data.text, 'lxml')
        #print(soup)
        ips = soup.find_all('tr')

        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[0].text + ':' + tds[1].text)
    return ip_list

def get_random_ip_kuaidaili(ip_list):
    '''
    获取满足条件的proxies_list。
    '''

    #test_url = ["https://www.taobao.com/", "https://www.baidu.com/", "https://www.tmall.com/", "https://www.jd.com/"]
    proxies_list = []
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    for i in range(len(proxy_list)):
        proxy_ip = proxy_list[i]
        proxies = {'http': proxy_ip}
        proxies_list.append(proxies)
        # num = 0
        # for x in range(len(test_url)):
        #
        #     res = requests.get(test_url[x], headers=headers, proxies=proxies)
        #     code =res.status_code
        #     if code == 200:
        #         num +=1
        # #print("num:",num)
        # if num == 4:
        #     proxies_list.append(proxies)
    #print(len(proxies_list))
    return proxies_list



if __name__ == '__main__':

    url = get_ip_url_kuaidaili()
    ip_list = get_ip_list_kuaidaili(url, headers)
    proxies_list_kuaidaili = get_random_ip_kuaidaili(ip_list)
    print(proxies_list_kuaidaili)


