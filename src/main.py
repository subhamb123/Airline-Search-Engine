
from algos.Spark_Queries import queryDataframe, filterDataframe,convertListToRoutes
from algos.Spark_Map import reduceWrapper,pathWrapper
from Ingestion.SparkIngestion import load_data
from Connector.WriteNeo4j import write_to_Neo4j
from Connector.ReadNeo4j import read_from_Neo4j
from pyspark.sql import SparkSession
from neo4j import GraphDatabase
import socketserver
import http.server
import os
import json
import sys



# sets the jar from maven repo for neo4j-connector-apache-spark
spark = (SparkSession.builder 
    .appName("Airline Data Processing") 
    .config("spark.jars.packages", "org.neo4j:neo4j-connector-apache-spark_2.12:5.2.0_for_spark_3")
    .config("spark.executor.cores", "4") 
    .getOrCreate())

# First load the data into spark dataframes for processing
use_reduced_data = False
# airport, airlines, routes = load_data(spark, use_reduced_data)



# Write the dataframes to AuraDB, commented out bc only need to write when performance testing
# write_to_Neo4j(airport, airlines, routes)

# Read from neo4j into DFs
airport, airlines, routes = read_from_Neo4j(spark)

# Initialize the driver to connect to Neo4j for queries
# driver = GraphDatabase.driver(new_uri, auth=(username, new_password))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'web/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("Data", post_data)
        post_data = json.loads(post_data)

        if self.path == '/data':
            response_data = self.handle_data_post(post_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def handle_data_post(self, data):
        result = {}
        time = 0
        if(data["function"] == "findAirline"):
            result, time = queryDataframe(df=airlines, conditions=json.loads(data["conditions"]))
        elif(data["function"] == "findAirports"):
            result,time = queryDataframe(df=airport, conditions=json.loads(data["conditions"]))
        # elif(data["function"] == "findRoutes"):
        #     result = queryDataframe(df=routes, conditions=json.loads(data["conditions"]))
        elif(data["function"] == "findDHopsCities"):
            conditions = json.loads(data["conditions"])
            result,time = reduceWrapper(airport, routes, int(data["Hop Count"]),filterDataframe(airport, conditions))
        elif(data["function"] == "findTrip"):
            source_airport = data.get("Source Airport")
            dest_airport = data.get("Destination Airport")
            result,time = pathWrapper(routes, source_airport, dest_airport)
            if result is None:
                return {}
            result.insert(0, source_airport)
            result = convertListToRoutes(routes,result)
        return {"result" : result, "time" : time}


PORT = 8080

web_dir = "."
os.chdir(web_dir)


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")

    # Start the server
    httpd.serve_forever()


