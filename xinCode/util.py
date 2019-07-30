#!/usr/bin/env python
# coding:utf-8
import configparser
import os
import random
import urllib3
from urllib.parse import urlparse
import json
import hashlib
from pymysql import connect

cf = configparser.ConfigParser()
cf.read("/web/spider/config/host.conf")

mysql_host = cf.get('Mysql', 'host')
mysql_user = cf.get('Mysql', 'user')
mysql_passwd = cf.get('Mysql', 'passwd')
mysql_db = cf.get('Mysql', 'db')
mysql_table_pdf_download = cf.get('Mysql', 'mysql_table_pdf_download')




user_agent_list = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_9_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.9.8; U; en) Presto/2.8.131 Version/11.11',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/24.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/24.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/24.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/24.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/24.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/24.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/24.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36"
]

def get_config(key):
    base_dir = os.path.dirname(__file__)
    configfile = os.path.join(base_dir, "../config/store_config.json")

    jsonfile = open(configfile)
    config = json.load(jsonfile)
    jsonfile.close()

    return config.get(key, None)


def safe_int(num, default=0):
    try:
        return int(num)
    except ValueError:
        result = []
        for c in num:
            if not ('0' <= c <= '9'):
                break
            result.append(c)
        if len(result) == 0:
            return default
        return int(''.join(result))


def get_random_ua():
    return user_agent_list[random.randint(0, len(user_agent_list)-1)]


def download_img(url, referer, dest_dir, file_name, ext='.jpg'):
    try:
        path = urlparse.urlparse(url).path
        ext_index = path.find('.', path.rfind('/'))
        if ext_index != -1:
            ext = path[ext_index:]
        file_name = file_name + ext
        req = urllib3.Request(url)
        req.add_header('Referer', referer)
        req.add_header('User-Agent', get_random_ua())
        resp = urllib3.urlopen(req, timeout=5)
        with open(os.path.join(dest_dir, file_name), 'w') as f:
            f.write(resp.read())
        return True, file_name
    except Exception as e:
        print('Exception: Fail to download from %s, %s' % (url, e))
        return False, ''


def is_absolute_url(url):
    return bool(urlparse.urlparse(url).netloc)


def get_absolute_url(url, referer):
    if is_absolute_url(url):
        return url
    else:
        return urlparse.urljoin(referer, url)


def make_index(str):
    md5 = hashlib.md5()
    md5.update(str.encode("utf-8"))
    return md5.hexdigest()


def mysql_tool(sql_query, arg):
    mysql_conn = connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, charset="utf8")
    cursor = mysql_conn.cursor()
    cursor.execute(sql_query, arg)
    mysql_conn.commit()
    cursor.close()
