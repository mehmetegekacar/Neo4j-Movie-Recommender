from neo4j import GraphDatabase
from py2neo import Graph
import pandas as pd
import numpy as np
import time 
from Functions.functions_for_based_on_atttributes import *
from Functions.matcheditdistance import *
import random


uri="neo4j+s://1c8f07f5.databases.neo4j.io"
username="neo4j"
password="uycJUUxlA1SDUncKIgImCp_DT8hASOiqSQ-V7pnLRCY"

tmdb = pd.read_csv('data\\tmdb_movies_data.csv')
ratings_test = pd.read_csv('data\\ratings_test.csv')
user_ids = ratings_test['userId'].unique()

def make_recommendations_collaborative_filtering(id, uri, username, password):
    graph = GraphDatabase.driver(uri, auth=(username, password))
    # User ID for whom you want to get recommendations
    target_user_id = id

    # Create a session
    with graph.session() as session:
        # Execute the Cypher query for recommendations
        query = """
        MATCH (targetUser:User {id: $target_user_id})-[:watched]->(ratedMovie:Movie)<-[:watched]-(similarUser:User)-[:watched]->(recommendedMovie:Movie)
        WHERE NOT (targetUser)-[:watched]->(recommendedMovie)
        WITH recommendedMovie, AVG(similarUser.popularity) AS predictedPopularity
        RETURN recommendedMovie, predictedPopularity
        ORDER BY predictedPopularity DESC
        LIMIT 20
        """
        result = session.run(query, target_user_id=target_user_id)

        liste = []
        # Process the result and print or use the recommendations
        for record in result:
            recommended_movie = record["recommendedMovie"]
            liste.append(recommended_movie["original_title"])

    # Close the Neo4j connection (not necessary with 'with' statement)
    graph.close()
    
    return liste

def make_recommendations_collaborative_popularitybased(id, uri, username, password):
    graph = GraphDatabase.driver(uri, auth=(username, password))
    # User ID for whom you want to get recommendations
    target_user_id = id

    # Create a session
    with graph.session() as session:
        # Execute the Cypher query for recommendations
        query = """
        MATCH (targetUser:User {id: $target_user_id})-[:watched]->(ratedMovie:Movie)<-[:watched]-(similarUser:User)-[:watched]->(recommendedMovie:Movie)
        WHERE NOT (targetUser)-[:watched]->(recommendedMovie)
        WITH recommendedMovie
        order by recommendedMovie.popularity desc
        RETURN distinct recommendedMovie
        LIMIT 20
        """
        result = session.run(query, target_user_id=target_user_id)

        liste = []
        # Process the result and print or use the recommendations
        for record in result:
            recommended_movie = record["recommendedMovie"]
            liste.append(recommended_movie["original_title"])

    # Close the Neo4j connection (not necessary with 'with' statement)
    graph.close()
    
    return liste


def make_recommendations_genre(id, uri, username, password):
    graph = GraphDatabase.driver(uri, auth=(username, password))
    # User ID for whom you want to get recommendations
    target_user_id = id

    # Create a session
    with graph.session() as session:
        # Execute the Cypher query for recommendations
        query = """
        MATCH (targetUser:User {id: $target_user_id})-[:watched]->(:Movie)-[:IN_GENRE]->(favoriteGenre:Genre)
        WITH targetUser, favoriteGenre, COUNT(*) AS genreCount
        ORDER BY genreCount DESC
        WITH targetUser, COLLECT(favoriteGenre)[0] AS favoriteGenre
        MATCH (recommendedMovie:Movie)-[:IN_GENRE]->(favoriteGenre)
        WHERE NOT (targetUser)-[:watched]->(recommendedMovie)
        WITH recommendedMovie
        ORDER BY recommendedMovie.popularity DESC
        RETURN recommendedMovie, recommendedMovie.popularity
        LIMIT 20;
        """
        result = session.run(query, target_user_id=target_user_id)

        liste = []
        # Process the result and print or use the recommendations
        for record in result:
            recommended_movie = record["recommendedMovie"]
            liste.append(recommended_movie["original_title"])

    # Close the Neo4j connection (not necessary with 'with' statement)
    graph.close()
    
    return liste



def make_recommendations_mostsimilar_knn(id, uri, username, password):
    graph = GraphDatabase.driver(uri, auth=(username, password))
    # User ID for whom you want to get recommendations
    target_user_id = id

    # Create a session
    with graph.session() as session:
        # Execute the Cypher query for recommendations
        query = """
        MATCH (targetUser:User {id: $target_user_id})-[:watched]->(commonMovie:Movie)<-[:watched]-(otherUser:User)-[:watched]->(m:Movie)
        WHERE NOT (m)<-[:watched]-(targetUser)
        WITH otherUser, COLLECT(DISTINCT m) AS commonMovies
        ORDER BY SIZE(commonMovies) DESC
        LIMIT 100

        UNWIND commonMovies AS commonMovie
        MATCH (otherUser:User)-[:watched]->(commonMovie)
        WITH commonMovie, COUNT(otherUser) AS userCount
        ORDER BY userCount DESC
        LIMIT 20

        RETURN commonMovie;
        """
        result = session.run(query, target_user_id=target_user_id)

        liste = []
        # Process the result and print or use the recommendations
        for record in result:
            recommended_movie = record["commonMovie"]
            liste.append(recommended_movie["original_title"])

    # Close the Neo4j connection (not necessary with 'with' statement)
    graph.close()
    
    return liste


def make_recommendations_favoritedirector(id, uri, username, password):
    graph = GraphDatabase.driver(uri, auth=(username, password))
    # User ID for whom you want to get recommendations
    target_user_id = id

    # Create a session
    with graph.session() as session:
        # Execute the Cypher query for recommendations
        query = """
        MATCH (targetUser:User {id: $target_user_id})-[:watched]->(commonMovie:Movie)<-[:DIRECTED]-(directors:Director)
        WITH targetUser, directors, COUNT(directors) AS dirCount
        ORDER BY dirCount DESC
        LIMIT 5

        unwind dirCount as dircount
        match (m)<-[:DIRECTED]-(directors)
        return m
        limit 20
        """
        result = session.run(query, target_user_id=target_user_id)

        liste = []
        # Process the result and print or use the recommendations
        for record in result:
            recommended_movie = record["m"]
            liste.append(recommended_movie["original_title"])

    # Close the Neo4j connection (not necessary with 'with' statement)
    graph.close()
    
    return liste


def make_recommendations_favoriteActor(id, uri, username, password):
    graph = GraphDatabase.driver(uri, auth=(username, password))
    # User ID for whom you want to get recommendations
    target_user_id = id

    # Create a session
    with graph.session() as session:
        # Execute the Cypher query for recommendations
        query = """
        MATCH (targetUser:User {id: $target_user_id})-[:watched]->(commonMovie:Movie)<-[:ACTED_IN]-(directors:Actor)
        WITH targetUser, directors, COUNT(directors) AS dirCount
        ORDER BY dirCount DESC
        LIMIT 5

        unwind dirCount as dircount
        match (m)<-[:ACTED_IN]-(directors)
        return m
        limit 20
        """
        result = session.run(query, target_user_id=target_user_id)

        liste = []
        # Process the result and print or use the recommendations
        for record in result:
            recommended_movie = record["m"]
            liste.append(recommended_movie["original_title"])

    # Close the Neo4j connection (not necessary with 'with' statement)
    graph.close()
    
    return liste

def precision_recall_f1_at_k(recommended_list, actual_list, k):
    # Take only the top-k recommended items
    recommended_list = recommended_list[:k]
    
    # Calculate the number of overlapping items between recommended and actual lists
    intersection = set(recommended_list) & set(actual_list)
    
    # Calculate precision
    precision = len(intersection) / len(recommended_list) if len(recommended_list) > 0 else 0.0
    
    # Calculate recall
    recall = len(intersection) / len(actual_list) if len(actual_list) > 0 else 0.0
    
    # Calculate F1 score
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return [precision, recall, f1]

def create_user_in_graph(user_ratings, tmdb):
    # Connect to the Neo4j database
    graph = GraphDatabase.driver(uri, auth=(username, password))

    # Create a session
    session = graph.session()

    for _, i in user_ratings.iterrows():
        id = i['userId']
        name = i['movieTitle']
        df = tmdb[tmdb['original_title'] == name]

        original_title = df["original_title"].values[0]
        release_date = df["release_date"].values[0]
        popularity = df["popularity"].values[0]

        query_to_create_user_add_rating = """
        MERGE (u:User {id: $id})
        WITH u
        MATCH (m:Movie {original_title: $original_title, release_date: $release_date, popularity: $popularity})
        MERGE (u)-[:watched]->(m)
        """

        parameters_genre = {
                    "original_title": original_title,
                    "release_date": release_date,
                    "popularity": popularity,
                    "id": id
                }
        session.run(query_to_create_user_add_rating, parameters_genre)

    # Close the session
    session.close()

    # Close the Neo4j connection
    graph.close()

def create_user(tmdb=tmdb):
    random_numbers = random.randrange(100000, 1000000)
    time.sleep(0.5)
    print("Enter your favorite movies: ")
    time.sleep(0.5)
    liste = ask_for_list()
    liste = closest_match_list(liste, movies)
    user_id = [random_numbers for _ in range(len(liste))]
    rating = pd.DataFrame(columns=["userId", "movieTitle"], data={"userId": user_id, "movieTitle": liste})
    create_user_in_graph(rating, tmdb)
    recommended = make_recommendations_mostsimilar_knn(id=random_numbers, uri=uri, username=username, password=password)
    return recommended