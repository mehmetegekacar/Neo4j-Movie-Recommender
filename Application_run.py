from Functions.prints import *
from Functions.matcheditdistance import *
import time
from neo4j import GraphDatabase
from py2neo import Graph
import pandas as pd
import numpy as np
from Functions.functions_for_based_on_atttributes import *
import warnings
import time 
from Functions.functions_for_based_on_atttributes import *
from Functions.matcheditdistance import *
from Functions.functions import *

warnings.filterwarnings("ignore")

while True:
    time.sleep(0.5)
    print(welcome_message)
    x = input("Press a key: ")
    if x == 'q':
        break
    else:
        if x == "1":
            time.sleep(0.5)
            print("How many movie do you want to be recommended?")
            number = input("Number of movies to be recommended: ")
            liste = create_user(tmdb)
            [print("selected movie => " , i) for i in liste[:int(number)]]



        if x=="2":
            time.sleep(0.5)
            print("How many movie do you want to be recommended?")
            number = input("Number of movies to be recommended: ")
            
            time.sleep(0.5)
            ask_genre_prompt()
            genre = ask_for_list()
            genre = closest_match_list(genre, genres)


            time.sleep(0.5)
            ask_director_prompt()
            director = ask_for_list()
            director = closest_match_list(director, directors)

            time.sleep(0.5)
            ask_actor_prompt()
            actor = ask_for_list()
            actor = closest_match_list(actor, actors)

            time.sleep(0.5)
            ask_year_prompt()
            start_year = input("Starting Year: ")
            end_year = input("Ending Year: ")
            

            time.sleep(0.5)
            print("Here are your recommendations: ...")
            all_names = get_pooling(genre, director, actor, uri, username, password)
            df = list_items(df, genre, director, actor, all_names, start_year, end_year)
            break
liste = df["original_title"].tolist()
[print("selected movie => " , i) for i in liste[:int(number)]]