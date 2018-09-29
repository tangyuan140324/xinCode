import configparser
import json

import time
from pykafka import KafkaClient
from pymongo import MongoClient


cf = configparser.ConfigParser()

cf.read("/web/spider/config/host.conf")

db_host = cf.get('db', 'db_host')

db_port = int(cf.get('db', 'db_port'))

redis_host = cf.get('redis','redis_host')

redis_port = int(cf.get('redis','redis_port'))

kafka_host = cf.get('kafka','kafka_host')

kafka_port = int(cf.get('kafka','kafka_port'))


def decorator(func):
    def showtime():
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    func()
    return showtime()

def connMongo(db_host, db_port):
    '''

    :param db_host: mongoDB主机IP地址
    :param db_port: mongoDB端口
    :return:
    '''

    conn = MongoClient(db_host ,db_port)
    db = conn.youzhi

    return db

def insertData(data, type ,tb):
    '''
    插入数据,传入三个参数
    :param data: 是要保存的数据单个的可以是字典格式{"":""}, 多个的以[{},{}]
    :param type: True表示单条数据存储 False 表示多条数据存储
    :param tb:   操作的表
    :return:
    '''

    if type is True:
        tb.insert(data)
    else :
        tb.insert_many(data)

def getTopic(host, port, topicname):
    '''
    获取话题
    :param host:      kafka主机ip
    :param port:      kafka端口
    :param topicname: 话题名称  传入参数是需要用b'test'方式  接受字节
    :return:          返回会话信息
    '''

    client = KafkaClient(hosts="%s:9092" %host)

    topic = client.topics[topicname]

    return topic

def getProducer(host, port, topicname):
    '''
    创建生产者,将数据发送到kafka
    :param host:     kafka主机IP
    :param port:     kafka主机端口
    :param topicname:  kafka会话名称
    :return:         返回创建的生产者
    '''

    topic = getTopic(host, port, topicname)

    producer = topic.get_producer()

    return producer
@decorator
def getConsumer(host, port, topicname, fromzook):#,zookhost
    '''
    创建消费者从kafka消费数据,默认直接消费kafka数据 如果formzook是True如果是False则从zookeeper消费数据
    :param host:        kafka主机ip地址
    :param port:        kafka端口
    :param topicname:   会话标识
    :param fromzook:    fromzook是True则默认从kafka获取数据
    :param zookhost:    zookeeper主机IP地址
    :return:            返回创建的消费者
    '''

    topic = getTopic(host, port, topicname)

    consumer = topic.get_simple_consumer(consumer_group=topicname)

    # if fromzook is True:
    #     consumer = topic.get_simple_consumer( auto_commit_enable=True,
    #                                          zookeeper_connect='%s:2181' % zookhost)
    return consumer
@decorator
def receiveData(consumer,db_host,db_port):
    '''
    消费者读取数据,同时将数据存入到mongoDB数据库中
    :param consumer:   消费者
    :param db_host:    数据库ip地址
    :param db_port:    数据库端口
    :return:
    '''

    db = connMongo(db_host,db_port)     #連接到mongo
    ### tb_productor: the collection is for taobao productor infomation.
    tb_productor = db.taobao
    ### tb_productor: the collection is for tmall productor infomation.
    tm_productor = db.tmall
    ### tb_productor: the collection is for shop infomation.
    shop_tb = db.taobaoshop
    ### tb_productor: the collection is for error infomation.
    error_tb = db.errordata
    ### tb_productor: the collection is for list infomation.
    list_tb = db.search_list
    ### tb_productor: the collection is for list infomation from taobao shop.
    taobao_list = db.taobao_list
    ### tb_productor: the collection is for list infomation from tmall shop.
    tmall_list = db.tmall_list
    for msg in consumer:
        consumer.commit_offsets()  #标记offset
        offset = msg.offset
        if msg is not None :
            #print(type(json.loads(msg.value,encoding="utf-8")))
            data =json.loads(msg.value,encoding="utf-8")
            print(data)
            print(type(data))
            data = eval(data)
            print("*******",type(data))
            print("seting to mongo:",data)

            # if type(data) is list:
            #     print("do this")
            #     for m in data:
            #         key = ""
            #         try:
            #             if "nid" in m.keys():
            #                 key = "Tmall" + m["nid"]
            #                 Api.saveTmallId(redis_host, redis_port, key, db=12)
            #                 insertData(m, True, tb)
            #             else:
            #                 insertData(data,True,error_tb)
            #         except AttributeError:
            #             print("没有该属性")

            try:
                if "dateType" in data.keys():
                    if data["dateType"] == "product":
                        if "attributes" in data.keys():
                            insertData(data, True, tb_productor)
                        else:
                            insertData(data,True,tm_productor)
                    elif data["dateType"] == "shop":
                        insertData(data, True, shop_tb)
                    elif data["dateType"] == "list":
                        if "totalSoldQuantity" in data.keys():
                            insertData(data, True, tmall_list)
                        else:
                            insertData(data, True, list_tb)
                    elif data['dateType'] == "taobao_list":
                        insertData(data, True, taobao_list)
                    else:
                        insertData(data, True, error_tb)

                else:
                    insertData(data,True,error_tb)

            except AttributeError:
                print("没有该属性")








if __name__ == "__main__":
    consumer = getConsumer(kafka_host,kafka_port,b'taobao',False)#,kafka_host
    receiveData(consumer,db_host,db_port)
