from kafka import KafkaConsumer

#consumer = KafkaConsumer(b'test', bootstrap_servers='192.168.211.198.9092')
consumer=KafkaConsumer('my_topic1',bootstrap_servers=['192.168.211.199:9092'])
for msg in consumer:
    print(msg.value)
    # recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    # print(recv)

