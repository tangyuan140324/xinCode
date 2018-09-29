#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import random
from bs4 import BeautifulSoup

from kuaidaili_proxy import get_ip_list_kuaidaili, get_random_ip_kuaidaili

headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }

proxy_out = []

def get_ip_url():
    '''
    创建一个随机的url

    '''
    beg_url = 'http://www.xicidaili.com/nn/'
    number = random.randint(0, 200)
    url = beg_url + str(number)
    print(url)
    return url


def get_ip_list(url, headers):
    '''
     在随机的url拿到当页的ip_proies.

    '''
    # url_kuaidaili = "https://www.kuaidaili.com/free/inha/1/"
    # ip_list = get_ip_list_kuaidaili(url_kuaidaili, headers)
    # proxies_list_kuaidaili = get_random_ip_kuaidaili(ip_list)
    # proxy = random.choice(proxies_list_kuaidaili)
    # print("proxy:",proxy)
    web_data = requests.get(url, headers=headers)
    print(web_data.status_code)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[0].text + ':' + tds[1].text)
    print("ip_list:",ip_list)
    return ip_list

def get_random_ip(ip_list):
    '''
    获取满足条件的proxies_list。
    '''

    test_url = ["https://www.taobao.com/", "https://www.baidu.com/", "https://www.tmall.com/", "https://www.jd.com/"]
    proxies_list = []
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    for i in range(len(proxy_list)):
        proxy_ip = proxy_list[i]
        proxies = {'http': proxy_ip}
        num = 0
        for x in range(len(test_url)):
            res = requests.get(test_url[x], headers=headers, proxies=proxies)
            code =res.status_code
            if code == 200:
                num +=1
        #print("num:",num)
        if num == 4:
            proxies_list.append(proxies)
    #print(len(proxies_list))
    return proxies_list



# def save_proxy(num,proxy):
#     '''
#     只选取测试4个网站通过的proxy添加进代理池
#
#     '''
#     proxies = json.dumps(proxy)
#     with open('agentPoll.txt','a') as f:
#         if num == 4 :
#             f.write(proxies+"\n")







if __name__ == '__main__':
    pass
    # client = redis.Redis("192.168.2.246", 6379, db=1)
    # for i in range(1, 100):
    #     url = get_ip_url()
    #     ip_list = get_ip_list(url, headers)
    #     num, proxy = get_random_ip(ip_list)
    #     client.set("agentPoll_use" + str(i), proxy)

    url = get_ip_url()
    ip_list = get_ip_list(url, headers)
    proxy = get_random_ip(ip_list)
    print(proxy)



