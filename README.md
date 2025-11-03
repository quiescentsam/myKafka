# Setup python env
uv venv .venv  
source .venv/bin/activate  
python -m ensurepip --upgrade  
python -m pip install kafka-python  

# start local cluster with Zookeeper and kafka
docker compose up -d 

## Create topic

docker exec -it kafka kafka-topics --create \
  --topic spark_test \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1




## list topic

docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092


# producer

docker exec -it kafka kafka-console-producer \
  --topic spark_test \
  --bootstrap-server localhost:9092


# consumer
docker exec -it kafka kafka-console-consumer \
  --topic spark_test \
  --from-beginning \
  --bootstrap-server localhost:9092


download jar from here
https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/4.0.1/


start pyspark 
pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1

>>> df = (spark.readStream
...       .format("kafka")
...       .option("kafka.bootstrap.servers", "localhost:9092")
...       .option("subscribe", "spark_test")
...       .option("startingOffsets", "earliest")
...       .load())
>>> 
>>> 
>>> df.show()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/opt/apache-spark/libexec/python/pyspark/sql/classic/dataframe.py", line 285, in show
    print(self._show_string(n, truncate, vertical))
  File "/usr/local/opt/apache-spark/libexec/python/pyspark/sql/classic/dataframe.py", line 303, in _show_string
    return self._jdf.showString(n, 20, vertical)
  File "/usr/local/opt/apache-spark/libexec/python/lib/py4j-0.10.9.9-src.zip/py4j/java_gateway.py", line 1362, in __call__
  File "/usr/local/opt/apache-spark/libexec/python/pyspark/errors/exceptions/captured.py", line 288, in deco
    raise converted from None
pyspark.errors.exceptions.captured.AnalysisException: Queries with streaming sources must be executed with writeStream.start();
kafka
>>> df.selectExpr("CAST(value AS STRING)").writeStream.format("console").start().awaitTermination()
25/10/30 16:36:58 WARN ResolveWriteToStream: Temporary checkpoint location created which is deleted normally when the query didn't fail: /private/var/folders/3q/kn__mcyj0bb7w4xj7rqwn8cc0000gn/T/temporary-e8adc366-da3f-4ad0-9973-a5ef5a253b31. If it's required to delete it under any circumstances, please set spark.sql.streaming.forceDeleteTempCheckpointLocation to true. Important to know deleting temp checkpoint folder is best effort.
25/10/30 16:36:58 WARN ResolveWriteToStream: spark.sql.adaptive.enabled is not supported in streaming DataFrames/Datasets and will be disabled.
-------------------------------------------                                     
Batch: 0
-------------------------------------------
+-----+
|value|
+-----+
|  hi |
|hello|
|  hey|
+-----+

-------------------------------------------
Batch: 1
-------------------------------------------
+-----+
|value|
+-----+
|this |
+-----+




# python producer
python kafka_producer.py

# spark consumer
spark-submit  --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 pyspark_kafka_consumer.py