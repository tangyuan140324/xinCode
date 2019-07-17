#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='192.168.211.199:9092')

msg = {
    "title" : "男装 高级轻型羽绒便携式V领背心 400500 优衣库UNIQLO",
    "view_price" : "199.00",
    "view_sales" : "375人付款",
    "nid" : "562119963188",
    "source_nid" : "562119963188",
    "detail_url" : "https://detail.tmall.com/item.htm?id=562119963188&ns=1&abbucket=0",
    "crawlDate" : "2018-05-02 17:45:09",
    "productType" : "羽绒背心",
    "item_loc" : "上海",
    "nick" : "优衣库官方旗舰店",
    "user_id" : "196993935",
    "dateType" : "list",
    "_meta" : {
        "store" : "mongodb"
    },
    "uz_id" : "92d4baf379dad354c27331ce36745e69",
    "img_urls": ['https://gd2.alicdn.com/imgextra/i4/647585155/TB2kiOKe_XYBeNkHFrdXXciuVXa_!!647585155.jpg','https://gd3.alicdn.com/imgextra/i3/647585155/TB2gTQXnb9YBuNjy0FgXXcxcXXa_!!647585155.jpg_50x50.jpg','https://gd4.alicdn.com/imgextra/i4/647585155/TB2wEThnf9TBuNjy0FcXXbeiFXa_!!647585155.jpg_50x50.jpg']
}

# 指定topic发送bytes类型的数据10001000
data = json.dumps(msg).encode(encoding="utf-8")
producer.send('my_topic1',data)
producer.flush()
producer.close()
print("OK")