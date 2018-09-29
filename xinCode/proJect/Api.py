#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import redis


wr = configparser.ConfigParser()
wr.read("/web/spider/config/host.conf")
host = wr.get('redis','redis_host')
port = int(wr.get('redis','redis_port'))
redisLog = '/web/spider/log/deWeightnid.log'
def log(recode):
    with open(redisLog,'a') as f:
        f.write(recode+',')


def Filter_Redis(host,port,str,db = 4):
    i = 0
    client = redis.Redis(host=host, port=port, db=db)
    isKey = client.exists(str)
    if isKey:
        i += 1
        log(str)
        return False
    else:
        return True


def saveTmallId(host,port,str,db = 5):
    client = redis.Redis(host=host, port=port, db=db)
    isKey = client.exists(str)
    if isKey:
        return False
    else:
        return True



def W_Shop_Id(host,port,str,db = 4):
    client = redis.Redis(host=host, port=port, db=db)
    client.set(str,"taobao", 72000)

def setTmallId(host,port,str,db = 5):
    client = redis.Redis(host=host, port=port, db=db)
    client.set(str,"Tmall",72000)

if __name__ =="__main__":
    pass
