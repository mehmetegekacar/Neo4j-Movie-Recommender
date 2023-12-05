from neo4j import GraphDatabase
from py2neo import Graph
import pandas as pd
import numpy as np

uri="neo4j+s://1c8f07f5.databases.neo4j.io"
username="neo4j"
password="uycJUUxlA1SDUncKIgImCp_DT8hASOiqSQ-V7pnLRCY"

df = pd.read_csv('data\\tmdb_movies_data.csv')
df = df[['original_title', 'release_date', 'genres', 'director', 'cast']]
df["cast"] = df["cast"].apply(lambda x: str(x))
df["cast"] = df["cast"].apply(lambda x: x.split("|"))
df["genres"] = df["genres"].apply(lambda x: str(x))
df["genres"] = df["genres"].apply(lambda x: x.split("|"))
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df = df[["original_title", "director","cast", "genres", "release_date"]]
df = df.dropna()

def check_cast(cast, actor_list):
    for actor in actor_list:
        if any(actor in item for item in cast):
            return 1
    return 0 
def check_date_interval(row, start_date, end_date):
    release_date = pd.to_datetime(row['release_date'], errors='coerce')
    return 1 if start_date <= release_date <= end_date else 0

def genreee(genre, uri, username, password):
    graph = GraphDatabase.driver(uri, auth=(username, password))

    # Create a session
    with graph.session() as session:
        # Execute the Cypher query for recommendations
        query = """
        MATCH (movie:Movie)-[:IN_GENRE]->(genre:Genre {name: $genre})
        RETURN movie
        ORDER BY movie.release_date DESC
        LIMIT 20;
        """
        result = session.run(query, genre=genre)

        liste = []
        # Process the result and print or use the recommendations
        for record in result:
            recommended_movie = record["movie"]
            liste.append(recommended_movie["original_title"])

    # Close the Neo4j connection (not necessary with 'with' statement)
    graph.close()
    
    return liste


def directorr(director, uri, username, password):
    graph = GraphDatabase.driver(uri, auth=(username, password))

    # Create a session
    with graph.session() as session:
        # Execute the Cypher query for recommendations
        query = """
        MATCH (director:Director {name: $director})-[:DIRECTED]->(movie:Movie)
        RETURN movie
        ORDER BY movie.release_date DESC
        LIMIT 20;
        """
        result = session.run(query, director=director)

        liste = []
        # Process the result and print or use the recommendations
        for record in result:
            recommended_movie = record["movie"]
            liste.append(recommended_movie["original_title"])

    # Close the Neo4j connection (not necessary with 'with' statement)
    graph.close()
    
    return liste

def actorr(actor, uri, username, password):
    graph = GraphDatabase.driver(uri, auth=(username, password))

    # Create a session
    with graph.session() as session:
        # Execute the Cypher query for recommendations
        query = """
        MATCH (actor:Actor {name: $actor})-[:ACTED_IN]->(movie:Movie)
        RETURN movie
        ORDER BY movie.release_date DESC
        LIMIT 10;
        """
        result = session.run(query, actor=actor)

        liste = []
        # Process the result and print or use the recommendations
        for record in result:
            recommended_movie = record["movie"]
            liste.append(recommended_movie["original_title"])

    # Close the Neo4j connection (not necessary with 'with' statement)
    graph.close()
    
    return liste



def get_pooling(genre, director, actor, uri, username, password):
    get_pooling = []
    for i in genre:
        aaa = genreee(i, uri, username, password)
        get_pooling.append(aaa)

    for i in director:
        aaa = directorr(i, uri, username, password)
        get_pooling.append(aaa)

    for i in actor:
        aaa = actorr(i, uri, username, password)
        get_pooling.append(aaa)
    all_names = []
    for i in get_pooling:
        if i!=[]:
            for j in i:
                all_names.append(j)
    return all_names

def list_items(df, genre, director, actor, all_names, start_date, end_date):
    empty_df = df[df['original_title'].isin(all_names)]
    empty_df["is_favorite_genre"] = empty_df.apply(lambda x: check_cast(x["genres"], genre), axis=1)
    empty_df["is_favorite_actor"] = empty_df.apply(lambda x: check_cast(x["cast"], actor), axis=1)
    empty_df["is_favorite_director"] = np.where(empty_df["director"].isin(director), 1, 0)
    start_date = pd.to_datetime(start_date, errors='coerce')
    end_date = pd.to_datetime(end_date, errors='coerce')
    empty_df['is_in_selected_date'] = empty_df.apply(lambda row: check_date_interval(row, start_date, end_date), axis=1)
    empty_df["overall_score"] = empty_df["is_favorite_director"] + empty_df["is_favorite_actor"] + empty_df["is_favorite_genre"] + empty_df['is_in_selected_date']
    empty_df.sort_values(by=['overall_score'], ascending=False, inplace=True)
    return empty_df
    