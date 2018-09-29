#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import random
from datetime import datetime
import redis
import requests
import time
import sched
from bs4 import BeautifulSoup


schedule = sched.scheduler(time.time,time.sleep)
#ip_poll = [{'http': 'http://115.223.231.181:9000'}, {'http': 'http://115.213.236.62:9000'}, {'http': 'http://106.111.243.41:9000'}, {'http': 'http://114.234.80.82:9000'}, {'http': 'http://115.193.103.23:9000'}, {'http': 'http://115.223.215.36:9000'}, {'http': 'http://115.223.229.233:9000'}, {'http': 'http://180.118.247.158:9000'}, {'http': 'http://220.191.71.56:9000'}, {'http': 'http://117.90.5.237:9000'}, {'http': 'http://125.117.134.179:9000'}, {'http': 'http://115.223.254.77:9000'}, {'http': 'http://114.234.83.126:9000'}, {'http': 'http://115.223.212.120:9000'}, {'http': 'http://115.223.234.248:9000'}, {'http': 'http://115.218.220.240:9000'}, {'http': 'http://115.223.234.42:9000'}, {'http': 'http://115.218.121.213:9000'}, {'http': 'http://122.242.86.189:9000'}, {'http': 'http://115.218.124.59:9000'}, {'http': 'http://163.125.251.183:8118'}, {'http': 'http://180.118.128.164:9000'}, {'http': 'http://115.213.239.110:9000'}, {'http': 'http://125.117.114.15:9000'}, {'http': 'http://121.232.199.222:9000'}, {'http': 'http://117.90.6.204:9000'}, {'http': 'http://115.223.233.232:9000'}, {'http': 'http://115.218.127.164:9000'}, {'http': 'http://115.223.213.144:9000'}, {'http': 'http://115.218.120.29:9000'}, {'http': 'http://180.118.73.86:9000'}, {'http': 'http://120.25.203.182:7777'}, {'http': 'http://115.223.193.53:9000'}, {'http': 'http://121.232.148.141:9000'}, {'http': 'http://115.218.123.102:9000'}, {'http': 'http://115.218.127.34:9000'}, {'http': 'http://122.243.15.45:9000'}, {'http': 'http://117.90.1.22:9000'}, {'http': 'http://121.232.148.32:9000'}, {'http': 'http://114.234.80.152:9000'}, {'http': 'http://114.234.83.245:9000'}, {'http': 'http://117.90.4.114:9000'}, {'http': 'http://114.234.81.50:9000'}, {'http': 'http://117.90.6.31:9000'}, {'http': 'http://115.223.198.17:9000'}, {'http': 'http://117.90.3.53:9000'}, {'http': 'http://115.223.227.54:9000'}, {'http': 'http://183.147.30.171:9000'}, {'http': 'http://121.232.194.212:9000'}, {'http': 'http://115.223.240.202:9000'}, {'http': 'http://115.218.124.223:9000'}, {'http': 'http://117.87.176.212:9000'}, {'http': 'http://121.232.194.109:9000'}, {'http': 'http://221.4.133.67:53281'}, {'http': 'http://115.223.224.36:9000'}, {'http': 'http://180.104.63.233:9000'}, {'http': 'http://115.223.228.69:9000'}, {'http': 'http://180.104.62.76:9000'}, {'http': 'http://115.223.194.15:9000'}, {'http': 'http://182.129.241.196:9000'}, {'http': 'http://180.118.247.89:9000'}, {'http': 'http://180.118.73.17:9000'}, {'http': 'http://122.243.11.255:9000'}, {'http': 'http://121.31.103.172:8123'}, {'http': 'http://115.223.221.178:9000'}, {'http': 'http://115.223.198.111:9000'}, {'http': 'http://171.37.157.81:8123'}, {'http': 'http://115.223.195.114:9000'}, {'http': 'http://115.223.214.116:9000'}, {'http': 'http://125.122.149.103:9000'}, {'http': 'http://115.218.126.213:9000'}, {'http': 'http://115.223.221.146:9000'}, {'http': 'http://117.90.1.48:9000'}, {'http': 'http://115.223.201.231:9000'}, {'http': 'http://115.223.193.163:9000'}, {'http': 'http://182.129.241.80:9000'}, {'http': 'http://163.125.221.75:8118'}, {'http': 'http://122.242.132.162:9000'}, {'http': 'http://222.132.56.80:9000'}, {'http': 'http://117.90.137.51:9000'}, {'http': 'http://180.118.86.169:9000'}, {'http': 'http://163.125.251.5:8118'}, {'http': 'http://115.223.215.30:9000'}, {'http': 'http://183.154.214.116:9000'}, {'http': 'http://58.87.87.142:80'}, {'http': 'http://117.78.50.121:8118'}, {'http': 'http://115.218.221.48:9000'}, {'http': 'http://180.118.128.153:9000'}, {'http': 'http://183.154.214.51:9000'}, {'http': 'http://125.117.133.214:9000'}, {'http': 'http://115.218.208.216:9000'}, {'http': 'http://115.223.246.151:9000'}, {'http': 'http://115.218.124.46:9000'}, {'http': 'http://182.88.187.248:8123'}, {'http': 'http://180.118.94.12:9000'}, {'http': 'http://115.218.126.115:9000'}, {'http': 'http://115.218.123.169:9000'}, {'http': 'http://180.104.62.46:9000'}, {'http': 'http://115.218.123.89:9000'}, {'http': 'http://115.218.216.121:9000'}, {'http': 'http://117.90.7.248:9000'}, {'http': 'http://114.234.80.166:9000'}, {'http': 'http://180.118.86.99:9000'}, {'http': 'http://163.125.251.9:8118'}, {'http': 'http://60.186.42.189:9000'}, {'http': 'http://115.223.233.43:9000'}, {'http': 'http://117.90.0.128:9000'}, {'http': 'http://115.223.254.151:9000'}, {'http': 'http://115.218.125.238:9000'}, {'http': 'http://106.4.135.252:9000'}, {'http': 'http://183.158.203.190:9000'}, {'http': 'http://115.211.40.164:9000'}, {'http': 'http://115.223.238.121:9000'}, {'http': 'http://118.117.136.123:9000'}, {'http': 'http://180.118.247.239:9000'}, {'http': 'http://111.3.108.44:8118'}, {'http': 'http://115.223.236.245:9000'}, {'http': 'http://115.223.200.60:9000'}, {'http': 'http://115.223.218.170:9000'}, {'http': 'http://36.7.111.92:8118'}, {'http': 'http://115.223.244.20:9000'}, {'http': 'http://115.223.253.40:9000'}, {'http': 'http://115.223.205.52:9000'}, {'http': 'http://115.223.216.143:9000'}, {'http': 'http://117.90.4.84:9000'}, {'http': 'http://115.218.223.238:9000'}, {'http': 'http://117.90.252.55:9000'}, {'http': 'http://115.193.101.168:9000'}, {'http': 'http://115.218.126.212:9000'}, {'http': 'http://115.223.229.114:9000'}, {'http': 'http://115.218.219.243:9000'}, {'http': 'http://125.119.217.255:9000'}, {'http': 'http://222.208.83.175:9000'}, {'http': 'http://117.90.3.66:9000'}, {'http': 'http://115.218.218.29:9000'}]
def get_ip_url():
    '''
    创建一个西祠代理url列表。

    '''
    beg_url = 'http://www.xicidaili.com/nn/'
    url_list = []
    for i in range(1,5):
        url = beg_url + str(i)
        url_list.append(url)
    print(url_list)
    return url_list

def get_ip_list(url_list):
    '''
    产出代理列表，并将符合要求的代理return。

    '''
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    proxy_list = []
    ip_list = []
    proxy_list_out = []
    for item in url_list:
        web_data = requests.get(item, headers=headers)
        time.sleep(1)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)
    for ip in ip_list:
        proxy_list_out.append('http://' + ip)
        if ip_list.index(ip) % 200 == 0:
            print(time.time())
    """
    for i in range(len(proxy_list)):
        proxy_ip = proxy_list[i]
        proxies = {'http': proxy_ip}
        num = 0
        needtimes = []
        for x in range(len(test_url)):
            beg = time.time()
            res = requests.get(test_url[x], headers=headers, proxies=proxies, verify=False)
            end = time.time()
            needtime = end - beg
            needtimes.append(needtime)
            if needtime <=0.09:
                time.sleep(0.5)
                code = res.status_code
                #print("checking validitiy of proxy",code)
                if code == 200:
                    num += 1
            if num == 3:
                proxy_list_out.append(proxies['http'])
                y = y+1
                #print("appending proxy to the list",y)

        #print(numpy.mean(needtimes))
        #print(numpy.std(needtimes))
        #print(numpy.percentile(needtimes, 60))
    # #print(proxy_list_out)
    """
    return proxy_list_out
    # for item in url_list:
    #     web_data = requests.get(item, headers=headers)
    #     time.sleep(1)
    #     soup = BeautifulSoup(web_data.text, 'lxml')
    #     ips = soup.find_all('tr')
    #     for i in range(1, len(ips)):
    #         ip_info = ips[i]
    #         tds = ip_info.find_all('td')
    #         ip_list.append(tds[1].text + ':' + tds[2].text)
    # for ip in ip_list:
    #     proxy_list.append('http://' + ip)
    # for i in range(len(proxy_list)):
    #     proxy_ip = proxy_list[i]
    #     proxies = {'http': proxy_ip}
    #     proxy_list_out.append(proxies)
    # return proxy_list_out

def redis_agent_poll(proxy_list_out,host = '127.0.0.1',port = 6379,db = 14):
    client = redis.Redis(host=host, port=port, db=db)
    client.set("agentPoll",proxy_list_out)
    print('存入redis成功...')
    print(datetime.now())

def execute_operate(inc):
    '''
    设置定时更新（30mins）。

    '''
    url_list = get_ip_url()
    proxy_list_out = get_ip_list(url_list)
    redis_agent_poll(proxy_list_out)
    schedule.enter(inc,0,execute_operate,[14400])

def main_start(inc=1):
    '''
    循环任务
    '''
    schedule.enter(0, 0, execute_operate, [14400])
    schedule.run()
if __name__ == '__main__':

    main_start()