from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def main():
    #creatre spark session, have to config because spark doesnt inclue kafka connector by default
    spark = SparkSession.builder \
        .appName("Forex Consumer") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
        .getOrCreate()
    print("Spark session created...")

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
    # and because kafka runs in docker, use kafka:9092 as the bootstrap server
    # and subscribe to the forex_topic -> read every new message sent there

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
        .select("data.*")  # Flatten the structure
    print("Data parsed from JSON...")

    #write the data to console
    query = parse_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .start()
    print("Writing data to console...")
    query.awaitTermination()  # Keep the stream running until terminated

if __name__ == "__main__":
    main()
    print("Forex consumer started...")