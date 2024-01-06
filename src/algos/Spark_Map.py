import time
import json
import sys
from pyspark.sql.functions import col,lower, udf
from pyspark.sql.functions import collect_list
from queue import Queue
from pyspark import SparkContext

def reduceWrapper(airport, routes,hop_count, starting_airports):
    tuple_starting = starting_airports.rdd.map(lambda row: (row['Airport ID'], row['City']))
    tuple_airports = airport.rdd.map(lambda row: (row['Airport ID'], row['City']))
    tuple_routes = routes.rdd.map(lambda row: (row['Source airport ID'], row['Destination airport ID'], row['Destination airport']))

    hops,time = reduceDHopsCities(tuple_airports, tuple_routes, hop_count, tuple_starting)
    result = {}
    for x in hops:
        result[x[1][1]] = min(x[1][0], result.get(x[1][1],sys.maxsize))
    result = [{"City" : k, "Level" :v} for k, v in sorted(result.items(), key=lambda item: item[1])]
    return result, time

def reduceDHopsCities(airports_rdd, routes_rdd, hop_count, starting_airports):
    if hop_count < 1:
        print("Invalid Hop Count")
        return
    start_time = time.time()

    current_level = starting_airports.map(lambda row: (row[0], 0))

    for i in range(1, hop_count + 1):
        next_level = current_level.join(routes_rdd).map(lambda row: (row[1][1], i))
        current_level = current_level.union(next_level).distinct()

    intersecting_rows = current_level.join(airports_rdd).distinct()
    intersecting_rows = sorted(intersecting_rows.collect(), key= lambda x:x[1][1])
    end_time = time.time()
    print(f"Spark find airlines in {hop_count} hops in: {end_time - start_time} seconds\n")

    # return intersecting_rows, end_time-start_time
    return intersecting_rows, end_time-start_time


def pathWrapper(routes, source_airport, dest_airport):
    sc = SparkContext.getOrCreate()

    # map
    tuple_routes = routes.rdd.map(lambda row: (row['Source airport'], row['Destination airport']))

    #reduce
    grouped_routes = tuple_routes.groupByKey().mapValues(list)

    # collect and broadcast across nodes
    routes_map = sc.broadcast(grouped_routes.collectAsMap())

    result,time = find_trip(routes_map,source_airport,dest_airport)
    return result,time

def find_trip(broadcasted_route_map, source_airport, destination_airport):
    visited = set()
    queue = Queue()
    start_time = time.time()
    queue.put((source_airport, []))  # (airport, path_to_airport)
    while not queue.empty():
        current_airport, path = queue.get()

        if current_airport == destination_airport:
            json_path = [row for row in path]
            end_time = time.time()
            print(f"Spark found routes in: {end_time - start_time} seconds\n")
            return json_path, end_time - start_time

        if current_airport in visited:
            continue
        visited.add(current_airport)

        next_routes = broadcasted_route_map.value.get(current_airport, [])
        for dest_airport in next_routes:
            if dest_airport not in visited:
                new_path = path + [dest_airport]
                queue.put((dest_airport, new_path))
    return None,None