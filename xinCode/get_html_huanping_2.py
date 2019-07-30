#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 下午2:19
# @Author  : dexin.Huang
# @File    : pyspider_zjhp_2019_07_11.py

import configparser
import logging
import os
from bs4 import BeautifulSoup
from pyspider.libs.base_handler import *
import re
import time
from util import make_index, mysql_tool

cf = configparser.ConfigParser()
cf.read("/web/spider/config/host.conf")
mysql_table_pdf_download = cf.get('Mysql', 'mysql_table_pdf_download')
mysql_table_html_download = cf.get('Mysql', 'mysql_table_html_download')

logging.basicConfig(level=logging.DEBUG,
                    filename='/data01/log/spider/huanping_2.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )
logger = logging.getLogger('result')



class Handler(BaseHandler):
    @every(minutes=5 * 24 * 60)
    def on_start(self):
        beg_url = 'http://www.zjepb.gov.cn/module/xxgk/search.jsp?divid=div1201347&infotypeId=A001AD001A001A001' \
                  '&jdid=1756&area=002482429&sortfield='
        self.crawl(beg_url, timeout=6, callback=self.zjhp_spiderUrls)

    @config(age=24 * 60 * 60)
    def zjhp_spiderUrls(self, response):
        total_page = re.findall(r'&nbsp;&nbsp;共(.*?)页&nbsp;', response.text, re.S)[0]
        url_list = []
        for i in range(1, int(total_page)+1):
            url = 'http://www.zjepb.gov.cn/module/xxgk/search.jsp?' \
                  'infotypeId=A001AD001&jdid=1756&area=&divid=div1201347&vc_title=&vc_number=&sortfield=,compaltedate:0&currpage={}' \
                  '&vc_filenumber=&vc_all=&texttype=&fbtime=&texttype=&fbtime=&vc_all=&vc_filenumber=&' \
                  'vc_title=&vc_number=&currpage={}&sortfield=,compaltedate:0'.format(str(i), str(i))
            url_list.append(url)
        self.crawl(url_list, timeout=6, callback=self.zjhp_condition_remains)


    @config(age=24 * 60 * 60)
    def zjhp_condition_remains(self, response):
        html_detail_tbody = BeautifulSoup(response.text, 'lxml')
        infos_list = []
        tbodys_one = html_detail_tbody.findAll("tr", class_='tr_main_value_even')
        tbodys_two = html_detail_tbody.findAll("tr", class_='tr_main_value_odd')
        for infos in tbodys_one + tbodys_two:
            html_info = {}
            if infos.a is not None:
                html_info["url"] = infos.a['href']
                self.crawl(infos.a['href'], save={'url': infos.a['href']}, timeout=6, callback=self.zjhp_parse_remains)
                html_info["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
                html_info["source"] = "浙江省生态环境厅"
                html_info["type"] = "huanping"
                path = "/data01/html/" + html_info["type"] + "/" + html_info["source"] +\
                       "/" + html_info["create_time"][0:10] + "/"
                id = make_index(html_info["url"] + path)
                html_info["path"] = path
                html_info["html_id"] = id
                html_info["status"] = 0
                html_info['topic'] = "html_info"
                sql = f"insert into {mysql_table_html_download}" \
                    f"(html_id,url,path,status,`type`,create_time) values (%s,%s,%s,%s,%s,%s)"
                mysql_tool(sql, [str(html_info["html_id"]), html_info["url"], html_info["path"],
                                    html_info["status"], html_info["type"], html_info["create_time"]])
                infos_list.append(html_info)
        return infos_list

    @config(age=24 * 60 * 60)
    def zjhp_parse_remains(self, response):
        data_list = []
        path_one = '/data01/html/huanping/浙江省生态环境厅/{}/'\
            .format(time.strftime("%Y-%m-%d"))
        if not os.path.exists(path_one):
            os.makedirs(path_one)
        path = path_one + make_index(response.save['url'])
        with open(path, 'w+') as f:
            f.write(response.text)
        oBject = BeautifulSoup(response.text, "html.parser")
        x = oBject.find("div", class_='mainContainer;').findAll('a')
        for i in range(len(x)):
            data_info = {}
            if 'Produced By 大汉网络 大汉版通发布系统' in x[i].getText():
                data_info['file_name'] = "UnknowPdfFile" + time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data_info['file_name'] = x[i].getText()[:-4]
            try:
                j = oBject.find("div", class_='mainContainer;').findAll('a')[i]['href']
                try:
                    url_part = re.findall(r"&filename=(.*?).pdf", j, re.S)[0]
                    if '/module/download/downfile.jsp?' in j:
                        data_info['file_url'] = ('http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files'
                                                 '/jcms1/web1756/site/attach/-1/{}.pdf'.format(url_part))
                    else:
                        data_info['file_url'] = url_part
                except IndexError:
                    url_part = 'http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web1756/site{}'\
                        .format(j)
                    data_info['file_url'] = url_part
                finally:
                    data_info["info"] = "this html can not get html info"
                    data_info["sub_url"] = response.save['url']
                    data_info["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    data_info["source"] = "浙江省环境生态厅"
                    data_info["pdf_id"] = make_index(data_info["file_url"] + data_info["sub_url"])
                    data_info["path"] = "/data01/pdf/"
                    data_info["status"] = 0
                    data_info["topic"] = "pdf_info"
                    sql_query = f"insert into {mysql_table_pdf_download}(info,sub_url,file_url,file_name,path," \
                        f"source,status,pdf_id,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    mysql_tool(sql_query, [str(data_info["info"]), data_info["sub_url"], data_info["file_url"],
                                           data_info["file_name"], data_info["path"], data_info["source"],
                                           data_info["status"], data_info["pdf_id"], data_info["create_time"]])
            except KeyError:
                logger.warning('this html has no pdf file')
            finally:
                data_list.append(data_info)
        return data_list






