#-*- coding:utf-8 -*-
# Author : 7secondsFish
# Data : 18-9-3 下午5:59

import logging
from pyspider.result import ResultWorker
from kafka import KafkaProducer
import json
import configparser

logger = logging.getLogger('result')

# wr = configparser.ConfigParser()
# wr.read("/web/spider/config/host.conf")
# kafka_host = wr.get('kafka','kafka_host')
# kafka_port = wr.get('kafka','kafka_port')
# kafka_server = kafka_host +":"+ kafka_port
#print(kafka_server)
class StoreWorker(ResultWorker):

    def __init__(self, resultdb, inqueue):
        logging.warning('in StoreWorker init')
        super(StoreWorker, self).__init__(resultdb, inqueue)
        self.producer = KafkaProducer(bootstrap_servers=["192.168.2.217:9092","192.168.2.218:9092"])
        print(self.producer.config)
        #print("hello")

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.producer.stop()




    def on_result(self, task, result):
        logger.warning("got result in StoreWorker --- ")
        resultlist = []
        if not result:
            return 'ERROR result'
        if isinstance(result,dict):
            resultlist.append(result)
        elif isinstance(result,list):
            resultlist = result
        for item in resultlist:
            data = bytes(json.dumps(item,ensure_ascii=False),encoding="utf-8")
            # if "img_urls" in item.keys():
            #     self.producer.send('downimg',data)
            # if len(item.keys()) != 3:
            #     self.producer.send("taobao1", data)
            if "want_job" in item.keys():
                self.producer.send('crawler_resume_qa', data)
            if 'virst_url' in item.keys():
                self.producer.send('crawler_comp_qa', data)
            if 'scheduling' in item.keys():
                self.producer.send('crawler_part_qa', data)
            if 'response_rates' in item.keys():
                self.producer.send('crawler_job_qa', data)
            self.producer.flush()