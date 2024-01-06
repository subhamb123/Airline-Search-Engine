import time

def write_to_Neo4j(airports_df, airlines_df, routes_df):
    # SSL Handshake error when connecting to AuraDB w/o self-signed cert
    # Docs for this connection with the self-signed cert: https://aura.support.neo4j.com/hc/en-us/articles/4405119907859-Handling-SSL-errors-when-connecting-to-your-AuraDB-Instance
    neo4j_uri = "neo4j+ssc://cdc70305.databases.neo4j.io"
    neo4j_password="2X4BWHyxDb7UGepmAfed1LfAUqw6hX1OV1mP-KIyisI"
    neo4j_username="neo4j"
    start_time = time.time()
    
    # Airline nodes
    (airlines_df.write.format("org.neo4j.spark.DataSource")
     .mode("Overwrite")
     .option("url", neo4j_uri)
     .option("authentication.type", "basic")
     .option("authentication.basic.username", neo4j_username)
     .option("authentication.basic.password", neo4j_password)
     .option("labels", "Airline")
     .option("node.keys", "Airline ID")
     .save())
    
    # airport nodes
    (airports_df.write.format("org.neo4j.spark.DataSource")
        .mode("Overwrite")
        .option("url", neo4j_uri)
        .option("authentication.type", "basic")
        .option("authentication.basic.username", neo4j_username)
        .option("authentication.basic.password", neo4j_password)
        .option("labels", "Airport")
        .option("node.keys", "Airport ID")
        .save())
    
    
    # Route relationships
    (routes_df.write.format("org.neo4j.spark.DataSource")
        .mode("Overwrite")
        .option("url", neo4j_uri)
        .option("authentication.type", "basic")
        .option("authentication.basic.username", neo4j_username)
        .option("authentication.basic.password", neo4j_password)
        .option("relationship", "ROUTE")
        .option("relationship.save.strategy", "keys")
        .option("relationship.source.labels", ":Airport")
        .option("relationship.source.save.mode", "Match")
        .option("relationship.source.node.keys", "Source airport ID:Airport ID")
        .option("relationship.target.labels", ":Airport")
        .option("relationship.target.save.mode", "Match")
        .option("relationship.target.node.keys", "Destination airport ID:Airport ID")
        .option("relationship.properties", "Airline, Airline ID, Codeshare, Stops, Equipment, RouteID, Source airport, Source airport ID, Destination airport, Destination airport ID")
        .save())
    
    end_time = time.time()
    print(f"Writing to Neo4j took: {end_time - start_time} seconds")
    
    print("Data written to AuraDB")