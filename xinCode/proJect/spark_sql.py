# -*- coding: utf-8 -*-
import os
import re

from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import when

#
#
#$os.environ ['JAVA_HOME'] = '/home/huangdexin/Downloads/JDK/jdk1.8.0_171'
#
# my_spark = SparkSession \
#     .builder \
#     .appName("myApp") \
#     .config("spark.mongodb.input.uri", "mongodb://192.168.2.213/youzhi.test") \
#     .config("spark.mongodb.output.uri", "mongodb://192.168.2.213/youzhi.test") \
#     .getOrCreate()
#
# df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
# print(df.columns)
# print(df)
# print(type(df))



# sparkSession = SparkSession.builder.appName("myApp").config("spark.mongodb.input.uri","mongodb://192.168.2.214/youzhi.taobao_list").config("spark.mongodb.output.uri","mongodb://192.168.2.214/youzhi.taobao").getOrCreate()
# df = sparkSession.read.format("com.mongodb.spark.sql.DefaultSource").load()
#
# def fun(str_data):
#     try:
#         views = re.search(r'[0-9]*', str(str_data), re.S)
#         data = int(views.group(0))
#     except :
#         data = -1
#     return data
# df1 = df.filter(df.nick != 'null')
#
# df1.createTempView("taobao")
#
# sparkSession.udf.register("f1",lambda x:fun(x))
#
# df2 = sparkSession.sql("from taobao select *,cast(f1(view_sales) as int) view")
#
# df2.filter(df2.view != -1).sort("view",ascending = False).show(100)
# df2.createTempView("taobao1")
# df3 = sparkSession.sql("from (from taobao1 select *,ROW_NUMBER() over(partition by nid order by crawlDate desc) as row) as a select a.* where a.row =1").sort("view",ascending = False).show()
#
#
#


sparkSession = SparkSession.builder.appName("myApp").config("spark.mongodb.input.uri","mongodb://192.168.2.214/youzhi.taobao_list").config("spark.mongodb.output.uri","mongodb://192.168.2.214/youzhi.taobao_list").getOrCreate()
df = sparkSession.read.format("com.mongodb.spark.sql.DefaultSource").load()
print(type(df))
df = df.filter(df.nick =="得体精品屋0708")
df = df.withColumnRenamed('_id', 'id').limit(1)

print(df.columns)
df.write.format("org.elasticsearch.spark.sql").option("es.resource", "dd/testDeXin").option("es.nodes", "192.168.2.214:9201").save()
