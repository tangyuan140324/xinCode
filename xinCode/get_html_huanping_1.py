#!/usr/bin/env python
# encoding: utf-8
'''
@author: fs
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/7/15 下午6:06
@desc:
'''
import configparser
import logging
import json
import os
import time
import traceback

from bs4 import BeautifulSoup
from pyspider.libs.base_handler import *
from util import make_index, mysql_tool
# Execute on the test server
with open("/web/spider/config/config.test.json", 'r') as f:
    data = json.loads(f.read())
    mysql_table_pdf_download = data['result_worker']['result_settings']['mysql_table_pdf_download']
    mysql_table_html_download = data['result_worker']['result_settings']['mysql_table_html_download']
# Execute locally
cf = configparser.ConfigParser()
cf.read("/web/spider/config/host.conf")
mysql_table_pdf_download = cf.get('Mysql', 'mysql_table_pdf_download')
mysql_table_html_download = cf.get('Mysql', 'mysql_table_html_download')

logging.basicConfig(level=logging.DEBUG,
                    filename='/data01/log/spider/huanping_1.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )
logger = logging.getLogger('result')


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(0, 50):
            if i == 0:
                self.crawl(url="http://hps.mee.gov.cn/jsxm/xmsl/index.shtml", callback=self.getItems)
            else:
                try:
                    self.crawl(url="http://hps.mee.gov.cn/jsxm/xmsl/index_"+str(i)+".shtml", callback=self.getItems)
                except Exception:
                    print(Exception)

    @catch_status_code_error
    @config(age=10 * 24 * 60 * 60)
    def getItems(self, response):
        datas=[]
        if response.status_code == 200:
            ob = BeautifulSoup(response.text, "html.parser")
            '''get list'''
            items = ob.find('div', class_="main_rt_list").findAll("li")
            for item in items:
                html_info = {}

                '''get a label'''
                click = item.find("a")
                if click != None:
                    href = str(click.attrs['href'])[1:]
                    if href.endswith(".shtml"):
                        url = "http://hps.mee.gov.cn/jsxm/xmsl" + str(click.attrs['href'])[1:]
                        self.crawl(url, save={'url': url}, timeout=6, callback=self.parser_html)
                        html_info["url"] = url
                        html_info["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        html_info["source"] = "中华人民共和国生态环境部"
                        html_info["status"] = 0
                        html_info["type"] = "huanping"
                        path = "/data01/html/" + html_info["type"] + "/" + html_info["source"] + \
                               "/" + html_info["create_time"][0:10] + "/"
                        id = make_index(html_info["url"] + path)
                        html_info["path"] = path
                        html_info["html_id"] = id
                        html_info['topic'] = "html_info"
                        sql = f"insert into {mysql_table_html_download}" \
                            f"(html_id,url,path,status,`type`,create_time) values (%s,%s,%s,%s,%s,%s)"
                        mysql_tool(sql, [str(html_info["html_id"]), html_info["url"], html_info["path"],
                                         html_info["status"], html_info["type"], html_info["create_time"]])
                    datas.append(html_info)
        return datas

    @catch_status_code_error
    @config(age=10 * 24 * 60 * 60)
    def parser_html(self, response):
        path_one = '/data01/html/huanping/中华人民共和国生态环境部/{}/'\
            .format(time.strftime("%Y-%m-%d"))
        if not os.path.exists(path_one):
            os.makedirs(path_one)
        path = path_one + make_index(response.save['url'])
        with open(path, 'w+') as f:
            f.write(response.text)
        ob = BeautifulSoup(response.text, "html.parser")
        obTime = ob.find('span', class_="wzxq_fbt2").findAll("p")[0].getText()
        timeList = str(obTime).replace("\n", "").strip().split("-")
        table = ob.findAll("table")
        keys = []
        flag = 1
        objs = []
        '''judge include table '''
        if len(table) != 0:
            '''table is include a lagel'''
            if len(table[0].findAll("a")) != 0:
                rows = table[0].findAll("tr")
                for row in rows:
                    if flag == 1:
                        '''deal first row data'''
                        for cell in row.findAll(['td', 'th']):
                            keys.append(str(cell.get_text()).replace("\n", "").strip())
                        flag += 1
                    else:
                        if len(row.findAll("a")) != 0:
                            '''judge row is include  a label'''
                            obj = {}
                            data = {}
                            try:
                                for i in range(0, len(keys)):
                                    obj[keys[i]] = str(row.findAll(['td', 'th'])[i].get_text()).replace("\n",
                                                                                                        "")
                                    fileUrl = "http://hps.mee.gov.cn/jsxm/xmsl/" + timeList[0] + timeList[
                                        1] + "/" + row.findAll("a")[0].attrs['oldsrc']
                                obj["项目名称"] = str(obj["项目名称"]).replace("/", "每").strip()
                            except:
                                logging.error({"error": traceback.format_exc(), "filePath": path,
                                               "time": time.strftime("%Y-%m-%d %H:%M:%S")})
                            finally:
                                data["info"] = json.dumps(obj, ensure_ascii=False)
                                data["sub_url"] = ob.find(attrs={"name": "Url"})['content']
                                data["file_url"] = fileUrl
                                data["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
                                data["source"] = "中华人民共和国生态环境部"
                                data["pdf_id"] = make_index(data["file_url"] + data["sub_url"])
                                data["file_name"] = obj["项目名称"]
                                data["path"] = "/data01/pdf/"
                                data["status"] = 0
                                data["topic"] = 'pdf_info'
                                objs.append(data)
                                sql = f"insert into {mysql_table_pdf_download}(info,sub_url,file_url," \
                                    f"file_name,path,source,status,pdf_id,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                mysql_tool(sql, [str(data["info"]), data["sub_url"], data["file_url"],
                                                 data["file_name"], data["path"], data["source"],
                                                 data["status"], data["pdf_id"],data["create_time"]])

        return objs