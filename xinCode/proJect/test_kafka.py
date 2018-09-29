# coding:utf-8
import json

from kafka import KafkaProducer, KafkaClient, KafkaConsumer

producer = KafkaProducer(bootstrap_servers=['192.168.2.91:9092'])

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
msg1 = json.dumps(msg)
data = bytes(msg1, encoding="utf8")
if "img_urls" in msg.keys():

    producer.send('downimg', data)
    print("ok")
if len(msg.keys()) != 3:
    producer.send("taobao1", data)
    print("ojbk")



consumer = KafkaConsumer('downimg',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        bootstrap_servers=['192.168.2.91:9092'])
for message in consumer:
# message value and key are raw bytes -- decode if necessary!
# e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
message.offset, message.key,
message.value))


# producer.send('test1', data)
# print('asd')
# producer.send('test2', data)
# print('fgg')
# producer.close()