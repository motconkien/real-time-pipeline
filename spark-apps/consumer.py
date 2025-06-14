from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os 
import json

USE_AWS = False
if USE_AWS:
    jdbc_url = "jdbc:postgresql://forex.cpg200e0ma98.ap-southeast-2.rds.amazonaws.com:5432/postgres"
    password =  'airflow123'
else:
    jdbc_url = "jdbc:postgresql://127.0.0.1:5432/postgres"
    password = 'root'
def write_to_postgres(batch_df, batch_id):
    try:
        print(f"Writing batch {batch_id} to Postgres... rows: {batch_df.count()}")
        batch_df.write \
            .format('jdbc') \
            .option('url', jdbc_url) \
            .option('dbtable', 'forex_data') \
            .option('user', 'postgres') \
            .option('password', password) \
            .option("driver", "org.postgresql.Driver") \
            .mode('append') \
            .save()
        print(f"Batch {batch_id} written successfully.")
    except Exception as e:
        print(f"Error writing batch {batch_id}: {e}")
        
def main():
     #creatre spark session, have to config cuz spark doesnt inclue kafka connector by default
     #if using s3 -> definitely need to config the hadoop conf when config spark session
    spark = SparkSession.builder \
        .appName("Forex Consumer") \
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.hadoop:hadoop-aws:3.3.4,org.postgresql:postgresql:42.5.4"
        ) \
        .getOrCreate()


    print("Spark session created...")

    #define output and if it is s3, remember to set the env variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY 
    output_data = "./output/forex_data"  
    # output_data = 's3a://real-time-pipeline-v1/forex_data'
    if output_data.startswith("s3a://"):
        with open("config.json",'r') as file:
            config = json.load(file)
        hadoop_conf = spark._jsc.hadoopConfiguration()
        hadoop_conf.set("fs.s3a.access.key", config.get('access_key'))
        hadoop_conf.set("fs.s3a.secret.key", config.get('secret_key'))
        hadoop_conf.set("fs.s3a.endpoint", "s3.ap-southeast-2.amazonaws.com")  # Thay vùng bucket bạn tạo

        # hadoop_conf.set("fs.s3a.endpoint", os.getenv('s3.amazonaws.com'))
    else:
        if not os.path.exists(output_data):
            os.makedirs(output_data)
        

    spark.sparkContext.setLogLevel("WARN")

    #define schema for the incoming data
    schema = StructType()\
        .add('timestamp', StringType()) \
        .add('currency_pair', StringType()) \
        .add('bid_price', FloatType()) \
        .add('ask_price', FloatType()) \
        .add('volume', IntegerType())
    print("Schema defined...")

    #read data from kafka topic amd format if it is not kafka, it might be csv, socket
    # and if kafka runs in docker, use kafka:9092 as the bootstrap server else localhost:9092
    # and subscribe to the forex_topic -> read every new message sent there and receicve the lastest one
    # if not subscribed, it is option('startingOffsets', 'earliest') -> consume all available messagese 

    forex_df = spark.readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', 'localhost:9092')\
        .option('subscribe', 'forex_topic') \
        .load()
    print("Data read from Kafka topic...")

    #load function will load the stream into df, 
    # # contain: key-b, value-b, top-str, partition-int, offset-long, timestamp, timestamptype-int
    
    # parse the value column as JSON and apply the schema
    parse_df = forex_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*") 
        
    print("Data parsed from JSON...")

    #write the data to console
    query = parse_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .start()
    print("Checking: Writing data to console...")

    #write the data to s3 bucket or local 
    aws_query = parse_df.writeStream \
            .outputMode("append") \
            .format("parquet") \
            .option("path", output_data) \
            .option("checkpointLocation", output_data + "_checkpoint") \
            .start()
    
    print(f"Writing data to {output_data}...")

    #write the data to postgres Mock DWH
    postgres_query = parse_df.writeStream \
                    .foreachBatch(write_to_postgres) \
                    .outputMode("append") \
                    .start()
    query.awaitTermination()  # Keep the stream running until terminated
    aws_query.awaitTermination(10)  # Keep the stream running until terminated
    postgres_query.awaitTermination()  # Keep the stream running until terminated


if __name__ == "__main__":
    main()
    print("Forex consumer started...")