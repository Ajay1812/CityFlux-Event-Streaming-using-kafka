from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType
from pyspark.sql.functions import from_json, col
from config import configuration

def main():
    spark = SparkSession.builder.appName("CityFlux-streaming")\
    .config("spark.jars.packages", 
             "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
            "org.apache.hadoop:hadoop-aws:3.3.1,"
            "com.amazonaws:aws-java-sdk:1.11.469") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
    .config("spark.hadoop.fs.s3a.access.key", configuration.get('AWS_ACCESS_KEY'))\
    .config("spark.hadoop.fs.s3a.secret.key", configuration.get('AWS_SECRET_KEY'))\
    .config("spark.hadoop.fs.s3a.credentials.provider", "org.apache.hadoop.fs.s3a.impl.SimpleAWSCredentialsProvider")\
    .getOrCreate()

    # Adjust the log level to minimize the console output on executors
    spark.sparkContext.setLogLevel('WARN')


    # Vehicle Schema
    vehicleSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", StringType(), True),
        StructField("make", StringType(), True),
        StructField("model", StringType(), True),
        StructField("year", IntegerType(), True),
        StructField("fuelType", StringType(), True)
        ])
    
    # GPS Schema
    gpsSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", StringType(), True),
        StructField("vehicleType", StringType(), True),
    ])

    # Traffic Schema
    trafficSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("cameraId", StringType(), True),
        StructField("location", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("snapshot", StringType(), True),
    ])

    # Weather Schema
    weatherSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("location", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("tempreture", DoubleType(), True),
        StructField("precipitation", DoubleType(), True),
        StructField("weatherCondition", StringType(), True),
        StructField("windSpeed", DoubleType(), True),
        StructField("humidity", IntegerType(), True),
        StructField("airQualityIndex", DoubleType(), True),
    ])

    # Emergency Schema
    emergencySchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("incidentId", StringType(), True),
        StructField("type", StringType(), True),
        StructField("location", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("status", StringType(), True),
        StructField("description", StringType(), True),
    ])

    def read_kakfa_topic(topic, schema):
        return (spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', 'broker:29092')
                .option('subscribe', topic)
                .option('startingOffset', 'earliest')
                .load()
                .selectExpr('CAST(value AS STRING)')
                .select(from_json(col('value'), schema).alias('data'))
                .select('data.*')
                .withWatermark('timestamp','5 minutes')
                )

    def streamWriter(input : DataFrame, checkpointFolder, output):
        return (input.writeStream
                .format('parquet')
                .option('checkPointLocation', checkpointFolder)
                .option('path', output)
                .outputMode('append')
                .start())

    vehicleDF = read_kakfa_topic('vehicle_data', vehicleSchema).alias('vehicle')
    gpsDF = read_kakfa_topic('gps_data', vehicleSchema).alias('gps')
    trafficDF = read_kakfa_topic('traffic_data', vehicleSchema).alias('traffic')
    weatherDF = read_kakfa_topic('weather_data', vehicleSchema).alias('weather')
    emergencyDF = read_kakfa_topic('emergency_data', vehicleSchema).alias('emergency')

    # Join all dfs with id and timestamp col
    # joinedDf

    query1 = streamWriter(vehicleDF, 
                 f's3a://{configuration.get('S3_BUCKET')}/checkpoints/vehicle_data',
                 f's3a://{configuration.get('S3_BUCKET')}/data/vehicle_data')
    query2 = streamWriter(gpsDF, 
                 f's3a://{configuration.get('S3_BUCKET')}/checkpoints/gps_data',
                 f's3a://{configuration.get('S3_BUCKET')}/data/gps_data')
    query3 = streamWriter(trafficDF, 
                 f's3a://{configuration.get('S3_BUCKET')}/checkpoints/traffic_data',
                 f's3a://{configuration.get('S3_BUCKET')}/data/traffic_data')
    query4 = streamWriter(weatherDF, 
                 f's3a://{configuration.get('S3_BUCKET')}/checkpoints/weather_data',
                 f's3a://{configuration.get('S3_BUCKET')}/data/weather_data')
    query5 = streamWriter(emergencyDF, 
                 f's3a://{configuration.get('S3_BUCKET')}/checkpoints/emergency_data',
                 f's3a://{configuration.get('S3_BUCKET')}/data/emergency_data')


    query5.awaitTermination()
if __name__ == "__main__":
    main()
