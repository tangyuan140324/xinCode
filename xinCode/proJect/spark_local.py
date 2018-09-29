# -*- coding: utf-8 -*-
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

# conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
# sc = SparkContext.getOrCreate(conf)

#（a）利用list创建一个RDD;使用sc.parallelize可以把Python list，NumPy array或者Pandas Series,Pandas DataFrame转成Spark RDD。
#rdd = sc.parallelize([1,2,3,4,5,6,7,8])
#print(rdd)
#Output:ParallelCollectionRDD[0] at parallelize at PythonRDD.scala:480

#（b）getNumPartitions()方法查看list被分成了几部分
#print(rdd.getNumPartitions())

#print(rdd.glom().collect())


spark = SparkSession.builder \
    .master("local") \
    .appName("Word Count") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
l = [('Alice', 1)]

#sc = spark.createDataFrame(l).collect()
sc = spark.createDataFrame(l, ['name', 'age']).collect()
print(sc)