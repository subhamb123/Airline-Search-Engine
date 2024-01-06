from neo4j import GraphDatabase
import json
import time


# Implementations of the Neo4j queries
def find_cities_reachable_within_d_hops(driver):
    current_city = input("Enter a city: ")
    hop_count = int(input("Enter a hop count: "))
    if(hop_count < 1):
        print("Hop count must be greater than 1")
        return
    cities = set()
    count = 1
    start = f"MATCH(a:`Source Airport`) WHERE a.City = '{current_city}'\n"
    middle = "MATCH (r0: Route {`Source airport` : a.IATA})-[g0]->(d0:`Destination Airport`)"
    end = "\nRETURN d0.City"
    while(count != hop_count):
        middle += f"\nMATCH (r{count}: Route {{`Source airport` : d{count-1}.IATA}})-[g{count}]->(d{count}:`Destination Airport`)\n"
        end += f",d{count}.City"
        count += 1
    with driver.session() as session:
        result = session.run(start+middle+end)
        for record in result:
            for r in record:
                cities.add(r)
        driver.close()
    if(len(cities) == 0):
        print("No hops found")
    else:
        print(len(cities), "cities found")


def find_airports_within_country(driver):
    start_time = time.time()
    country = input("Enter a country: ")
    with driver.session() as session:
        result = session.run(f"""MATCH (a:Airport)
                                WHERE a.Country = '{country}'
                                RETURN a""")
        for record in result:
            print(record[0]['Name'])
        driver.close()
    end_time = time.time()
    print(f"Find airports within country took: {end_time - start_time} seconds")