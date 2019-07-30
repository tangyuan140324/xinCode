#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 下午7:53
# @Author  : dexin.Huang
# @File    : savePdf.py

import configparser
import json
import logging
import os

import requests
from kafka import KafkaConsumer
from pymysql import *
# import sys, os
# BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_PATH)
from dataToMongo import getConsumer

cf = configparser.ConfigParser()
cf.read("/web/spider/config/host.conf")
kafka_host = cf.get('kafka', 'kafka_host')
kafka_port = cf.get('kafka', 'kafka_port')
kafka_topic_pdf_download = cf.get('kafka', 'kafka_topic_pdf_download')

mysql_host = cf.get('Mysql', 'host')
mysql_user = cf.get('Mysql', 'user')
mysql_passwd = cf.get('Mysql', 'passwd')
mysql_db = cf.get('Mysql', 'db')
mysql_table_pdf_download = cf.get('Mysql', 'mysql_table_pdf_download')

logging.basicConfig(level=logging.DEBUG,
                    filename='/data01/log/spider/savePdf.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )
logger = logging.getLogger('result')


def connKafak(topic_name):
    consumer = KafkaConsumer(topic_name, bootstrap_servers=['{}:{}'.format(kafka_host, kafka_port)])
    logger.info('connect to kafka sucess!')
    return consumer


def main(consumer, mysql_conn):
    for msg in consumer:
        consumer.commit_offsets()
        if msg is not None:
            data = json.loads(msg.value, encoding="utf-8")
            savePath = data['path']
            if not os.path.exists(savePath):
                os.makedirs(savePath)
            url = data['file_url']
            pdf_id = data['pdf_id']
            fileName = data['file_name']
            save_path = savePath + fileName + '.pdf'
            if not os.path.exists(save_path):
                res = requests.get(url, timeout=60)
                try:
                    with open(save_path, 'wb+') as f:
                        f.write(res.content)
                except OSError:
                    with open(savePath + fileName[:4:] + '.pdf', 'wb+') as f:
                        f.write(res.content)
                finally:
                    cursor = mysql_conn.cursor()
                    sql = f"""update {mysql_table_pdf_download} set status = 1 where pdf_id="%s" """ % (pdf_id)
                    cursor.execute(sql)
                    mysql_conn.commit()
            else:
                logging.warning('The current directory already exists, no action is required')
            logger.info('sucessfully download pdf data!')
        else:
            logging.warning('No information received from kafka')


if __name__ == '__main__':
    mysql_conn = connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db,
                         charset="utf8")
    consumer = getConsumer(kafka_host, kafka_port, bytes(kafka_topic_pdf_download, encoding="utf8"), False, kafka_host)
    main(consumer, mysql_conn=mysql_conn)
