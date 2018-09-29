#!/usr/bin/env python3
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
sc.textFile("hdfs://192.168.2.246:9001/test",use_unicode = False).foreach(lambda x:print(x))
# li = ["1","hello","world",'sb']
# sc.parallelize(li).saveAsTextFile("hdfs://192.168.2.244:9001/test/result4")
