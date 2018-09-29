# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession

sparkSession = SparkSession\
    .builder.appName("myApp")\
    .config("spark.mongodb.input.uri","mongodb://192.168.2.213/youzhi.taobao_list")\
    .config("spark.mongodb.output.uri","mongodb://192.168.2.213/youzhi.taobao_list")\
    .getOrCreate()

df = sparkSession.read.format("com.mongodb.spark.sql.DefaultSource").load()


df.createTempView("xiaoliangpaixu")
df2 = sparkSession.sql("from xiaoliangpaixu select *,cast(act as int) view")
df3 = df2.filter(df2.view != -1).sort("view",ascending = False).drop("_id").limit(100).show(10)


#df3.write.format("org.elasticsearch.spark.sql").option("es.resource", "dx/testDeXin").option("es.nodes", "192.168.2.246:9200").save()

