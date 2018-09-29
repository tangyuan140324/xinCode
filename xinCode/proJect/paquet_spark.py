# -*- coding: utf-8 -*-


from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext


sparkSession = SparkSession.builder.appName('sb').getOrCreate()
df = sparkSession.read.parquet("hdfs://192.168.2.210:9000/UZ/Tmall/search_list/2018/05/08/18")
#df.printSchema()

df.show()

'''
读取text文件。
conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
sc.textFile("hdfs://192.168.2.210:9000/UZ/Taobao/list/*/*/*/*/*",use_unicode = False).foreach(lambda x:print(x))
'''

