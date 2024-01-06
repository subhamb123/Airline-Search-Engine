from pyspark.sql.functions import col,lower, udf
import json
import time
from pyspark.sql.functions import lit
from queue import Queue
from pyspark.sql.types import IntegerType

from pyspark.sql.functions import collect_list

def queryDataframe(df, conditions):
    start_time = time.time()

    result_df = df

    for key, value in conditions.items():
        result_df = result_df.filter(lower(col(key)) == value.lower())
    end_time = time.time()

    return result_df.toJSON().map(lambda j: json.loads(j)).collect(), end_time - start_time


def filterDataframe(df, conditions):
    result_df = df

    for key, value in conditions.items():
        result_df = result_df.filter(lower(col(key)) == value.lower())

    return result_df


def filterRDD(rdd, conditions):
    for key, value in conditions.items():
        rdd = rdd.filter(lambda x: x[key].lower() == value.lower())
    rdd = rdd.map(lambda x : (x,1))
    return rdd


def convertListToRoutes(routes_df, routes):
    filter_conditions = [
    (col("Source airport") == routes[i]) & (col("Destination airport") == routes[i + 1])
    for i in range(len(routes) - 1)]

    combined_condition = filter_conditions[0]
    for condition in filter_conditions[1:]:
        combined_condition = combined_condition | condition

    selected_routes_df = routes_df.filter(combined_condition)
    selected_routes_df = selected_routes_df.dropDuplicates(["Source airport", "Destination airport"])
    index_udf = udf(lambda x: routes.index(x), IntegerType())
    selected_routes_df = selected_routes_df.withColumn("index", index_udf(col("Source airport")))
    # selected_routes_df = selected_routes_df.orderBy(keyFunc=lambda x : routes.index(x["Source Airport"]))
    selected_routes_df = selected_routes_df.orderBy("index")
    selected_routes_df = selected_routes_df.drop("index")
    return selected_routes_df.toJSON().map(lambda j: json.loads(j)).collect()



# Original algorithms, deprecated since the filterRDD and filterDataframe

# def country_most_airports(airports_df):
#     start_time = time.time()
#     airports_in_country = (airports_df.groupBy(airports_df.schema.names[3]).count()).orderBy(col("count").desc())
#     airports_in_country.limit(1).show()
#     end_time = time.time()
#     print(f"Spark algorithm took: {end_time - start_time} seconds\n")


# def find_airports_within_country(airports_df, country):
#     country = country.lower()
#     start_time = time.time()
#     airports_in_country = airports_df.filter(lower(airports_df["Country"]) == country)
#     end_time = time.time()
#     print(f"Airport count: {airports_in_country.count()}")
#     print(f"Spark find airports within country took: {end_time - start_time} seconds\n")
#     return airports_in_country.toJSON().map(lambda j: json.loads(j)).collect()