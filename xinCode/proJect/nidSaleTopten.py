# -*- coding: utf-8 -*-
import re
from pyspark.sql import SparkSession

# Custom function:
def fun(str_data):
    try:
        views = re.search(r'[0-9]*', str(str_data), re.S)
        data = int(views.group(0))
    except :
        data = -1
    return data

sparkSession = SparkSession.builder.appName('spark').getOrCreate()
df = sparkSession.read.parquet("hdfs://192.168.2.210:9000/UZ/Taobao/list/*/*/*/*")\
    .selectExpr("*","ROW_NUMBER() over(partition by nid order by crawlDate) row")

df = df.filter(df.row == 1)


df1 = sparkSession.read.parquet("hdfs://192.168.2.210:9000/UZ1/Tmall/list/*/*/*/*")\
    .selectExpr("*","ROW_NUMBER() over(partition by nid order by crawlDate) row")
df1 = df1.filter(df1.row == 1)

sparkSession.udf.register("f1",lambda x:fun(x))

df2 = df1.selectExpr("nid","title","cast(f1(sold) as int) act","price","crawlDate")\
    .unionAll(df.select("nid","title","act","price","crawlDate"))\
    .sort('act',ascending = False)\
    .limit(100)

'''
write to ElasticSearch.
'''
df2.write.format("org.elasticsearch.spark.sql")\
    .option("es.resource", "dxsaletopten1/testDeXin")\
    .option("es.nodes", "192.168.2.246:9200")\
    .save()


if __name__ =="__main__":
    pass