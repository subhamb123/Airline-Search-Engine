from pyspark.sql import SparkSession
from Ingestion.SparkSchema import SparkSchema
from Ingestion.DataConfig import DataConfig
from pyspark.sql.functions import col, when, count
import time

def load_data(spark, use_reduced_data):
    start_time = time.time()
    # read the csv files into dataframes
    airports_df = spark.read.csv(
        DataConfig.get_path("airports", use_reduced_data),
        header=True,
        mode="DROPMALFORMED",
        schema=SparkSchema.airport_schema
    )

    airlines_df = spark.read.csv(
        DataConfig.get_path("airlines", use_reduced_data),
        header=True,
        mode="DROPMALFORMED",
        schema=SparkSchema.airline_schema
    )

    routes_df = spark.read.csv(
        DataConfig.get_path("routes", use_reduced_data),
        header=True,
        mode="DROPMALFORMED",
        schema=SparkSchema.route_schema
    )
    
    end_time = time.time()
    print(f"Spark data ingestion took: {end_time - start_time} seconds")
    return airports_df, airlines_df, routes_df

