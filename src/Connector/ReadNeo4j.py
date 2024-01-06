from Ingestion.SparkSchema import SparkSchema
from pyspark.sql import SparkSession
from pyspark.sql.types import *

NEO4J_URI = "neo4j+ssc://cdc70305.databases.neo4j.io"
NEO4J_PASSWORD="2X4BWHyxDb7UGepmAfed1LfAUqw6hX1OV1mP-KIyisI"
NEO4J_USERNAME="neo4j"

def spark_Read_Query(spark, query, schema):
    return (spark.read.format("org.neo4j.spark.DataSource")
            .option("url", NEO4J_URI)
            .option("authentication.basic.username", NEO4J_USERNAME)
            .option("authentication.basic.password", NEO4J_PASSWORD)
            .option("query", query)
            .schema(schema)
            .load())

def read_from_Neo4j(spark):
    airport_query = '''
        MATCH (a:Airport)
        RETURN a.`Airport ID` AS `Airport ID`, a.Name AS Name, a.City AS City, a.Country AS Country, 
        a.IATA AS IATA, a.ICAO AS ICAO, a.Latitude AS Latitude, a.Longitude AS Longitude, a.Altitude AS Altitude, 
        a.Timezone AS Timezone, a.DST AS DST, a.`Tz database time zone` AS `Tz database time zone`, a.Type AS Type, a.Source AS Source
    '''
    
    airline_query = '''
        MATCH (a:Airline)
        RETURN a.`Airline ID` AS `Airline ID`, a.Name AS Name, a.Alias AS Alias, a.IATA AS IATA,
        a.ICAO AS ICAO, a.Callsign AS Callsign, a.Country AS Country, a.Active AS Active
    '''
    
    route_query = '''
        MATCH (source: Airport)-[r:ROUTE]->(dest:Airport)
        RETURN r.RouteID AS RouteID, r.Airline AS Airline, r.`Airline ID` AS `Airline ID`,
        r.`Source airport` AS `Source airport`, r.`Source airport ID` AS `Source airport ID`,
        r.`Destination airport` AS `Destination airport`, r.`Destination airport ID` AS `Destination airport ID`, 
        r.Codeshare AS Codeshare, r.Stops AS Stops, r.Equipment AS Equipment
    '''

    airport_df = spark_Read_Query(spark, airport_query, SparkSchema.airport_schema)
    airlines_df = spark_Read_Query(spark, airline_query, SparkSchema.airline_schema)
    routes_df = spark_Read_Query(spark, route_query, SparkSchema.route_schema)

    return airport_df, airlines_df, routes_df
