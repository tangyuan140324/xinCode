# !/usr/bin/env python
# -*- encoding: utf-8 -*-
import configparser


from pykafka import KafkaClient

cf = configparser.ConfigParser()

cf.read("/web/spider/config/host.conf")

db_host = cf.get('db', 'db_host')

db_port = int(cf.get('db', 'db_port'))

redis_host = cf.get('redis','redis_host')

redis_port = int(cf.get('redis','redis_port'))

kafka_host = cf.get('kafka','kafka_host')

kafka_port = int(cf.get('kafka','kafka_port'))



def getData(data,tb):
    '''

    :param data: 查询条件，dict
    :param tb: 查询表
    :return:
    '''
    return tb.find(data)
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

def getConsumer(host, port, topicname, fromzook,zookhost):
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

    if fromzook is True:
        consumer = topic.get_simple_consumer( auto_commit_enable=True,
                                             zookeeper_connect='%s:2181' % zookhost)
    return consumer
