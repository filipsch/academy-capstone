from pathlib import Path
from typing import Collection, Mapping, Union
from pyspark import SparkConf
from pyspark.sql import Column, DataFrame, SparkSession
import pyspark.sql.functions as psf
from pyspark.sql.types import (
    TimestampType,
    BooleanType,
    IntegerType,
)
import boto3
import json
from dotenv import load_dotenv
import os
import logging

AWS_URL = "s3a://dataminded-academy-capstone-resources/raw/open_aq/"
CREDS_NAME = 'snowflake/capstone/config'
SF_SCHEMA_NAME = 'FILIP'
TARGET_TABLE_NAME = 'measurements'

def clean_data(frame: DataFrame) -> DataFrame:
    return (
        frame
        .withColumn('latitude', psf.col('coordinates.latitude'))
        .withColumn('longitude', psf.col('coordinates.longitude'))
        .drop('coordinates')
        .withColumn('measured_at', psf.col('date.utc').cast(TimestampType()))
        .drop('date')
        .withColumnRenamed('country', 'country_code')
        .withColumnRenamed('isAnalysis', 'is_analysis')
        .withColumn('is_analysis', psf.col('is_analysis').cast(BooleanType()))
        .withColumnRenamed('isMobile', 'is_mobile')
        .withColumn('is_mobile', psf.col('is_mobile').cast(BooleanType()))
        .withColumnRenamed('locationId', 'location_id')
        .withColumn('location_id', psf.col('location_id').cast(IntegerType()))
        .withColumnRenamed('sensorType', 'sensorType')
        .withColumnRenamed('city', 'province')
    )

def get_snowflake_config(name: str):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=os.environ.get('AWS_REGION', 'eu-west-1'))
    secrets_list = client.list_secrets(Filters=[{'Key': 'name', 'Values': [name]}])
    secret = client.get_secret_value(SecretId = secrets_list['SecretList'][0]['ARN'])
    secrets =  json.loads(secret['SecretString'])
    return {
        "sfURL": secrets.get("URL"),
        "sfUser": secrets.get("USER_NAME"),
        "sfPassword": secrets.get("PASSWORD"),
        "sfDatabase": secrets.get("DATABASE"),
        "sfWarehouse": secrets.get("WAREHOUSE"),
        "sfSchema": SF_SCHEMA_NAME,
    }
    
def load_data(frame: DataFrame):
    pass    

if __name__ == "__main__":
    if Path("local_data").exists():
        logging.info(">>>>> Fetching data from local folder...")
        config = {
            "spark.jars.packages":"net.snowflake:spark-snowflake_2.12:2.9.0-spark_3.1,net.snowflake:snowflake-jdbc:3.13.3"
        }
        conf = SparkConf().setAll(config.items())
        spark = SparkSession.builder.config(conf=conf).getOrCreate()
        spark = SparkSession.builder.getOrCreate()
        frame = spark.read.parquet("local_data")
    else:
        # Load environment variables
        load_dotenv()
        logging.info(">>>>> Fetching data from AWS S3...")
        config = {
            "spark.jars.packages":"net.snowflake:spark-snowflake_2.12:2.9.0-spark_3.1,net.snowflake:snowflake-jdbc:3.13.3,org.apache.hadoop:hadoop-aws:3.2.0",
            "spark.hadoop.fs.s3a.aws.credentials.provider": "com.amazonaws.auth.DefaultAWSCredentialsProviderChain"
        }
        conf = SparkConf().setAll(config.items())
        spark = SparkSession.builder.config(conf=conf).getOrCreate()
        frame = spark.read.json(
            AWS_URL,
            primitivesAsString=True,
        )
        frame.write.parquet(path="local_data",mode="overwrite",compression="snappy")
        # from utils import assert_frames_functionally_equivalent
        # assert_frames_functionally_equivalent(frame, frame2)

    spark.sparkContext.setLogLevel("ERROR")
    logging.info(">>>>> Cleaning data...")
    clean_frame = clean_data(frame)

    # Write DataFrame to Snowflake
    logging.info(">>>>> Writing to snowflake...")
    clean_frame.write.format("net.snowflake.spark.snowflake") \
        .options(**get_snowflake_config(CREDS_NAME)) \
        .option("dbtable", TARGET_TABLE_NAME) \
        .mode("overwrite") \
        .save()

    logging.info(">>>>> Finished!")
