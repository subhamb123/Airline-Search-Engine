from pyspark.sql.types import *

# Schema for spark dataframes
class SparkSchema:

    airport_schema = StructType([
        StructField("Airport ID", LongType(), True),
        StructField("Name", StringType(), True),
        StructField("City", StringType(), True),
        StructField("Country", StringType(), True),
        StructField("IATA", StringType(), True),
        StructField("ICAO", StringType(), True),
        StructField("Latitude", DoubleType(), True),
        StructField("Longitude", DoubleType(), True),
        StructField("Altitude", LongType(), True),
        StructField("Timezone", LongType(), True),
        StructField("DST", StringType(), True),
        StructField("Tz database time zone", StringType(), True),
        StructField("Type", StringType(), True),
        StructField("Source", StringType(), True)
    ])

    airline_schema = StructType([
        StructField("Airline ID", LongType(), True),
        StructField("Name", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("IATA", StringType(), True),
        StructField("ICAO", StringType(), True),
        StructField("Callsign", StringType(), True),
        StructField("Country", StringType(), True),
        StructField("Active", StringType(), True)
    ])

    route_schema = StructType([
        StructField("RouteID", LongType(), True),
        StructField("Airline", StringType(), True),
        StructField("Airline ID", LongType(), True),
        StructField("Source airport", StringType(), True),
        StructField("Source airport ID", LongType(), True),
        StructField("Destination airport", StringType(), True),
        StructField("Destination airport ID", LongType(), True),
        StructField("Codeshare", StringType(), True),
        StructField("Stops", LongType(), True),
        StructField("Equipment", StringType(), True)
    ])