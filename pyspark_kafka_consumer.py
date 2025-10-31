from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

# Kafka broker
BROKER = 'localhost:9092'
TOPIC = 'spark_test'

# Create SparkSession
spark = (SparkSession.builder
         .appName("KafkaConsumer")
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1")
         .getOrCreate())

# Define JSON schema
schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("event", StringType()),
    StructField("amount", DoubleType())
])

# Read stream from Kafka
df = (spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", BROKER)
      .option("subscribe", TOPIC)
      .option("startingOffsets", "earliest")
      .load())

# Parse JSON messages
json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Output to console
query = (json_df.writeStream
         .format("console")
         .outputMode("append")
         .start())

query.awaitTermination()
