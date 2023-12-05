import pandas as pd
import numpy as np
import editdistance

df = pd.read_csv('data\\tmdb_movies_data.csv')
actors = df['cast'].unique()
directors = df['director'].unique()
genres = df['genres'].unique()
movies = df['original_title'].unique()


def ask_for_list():
    liste = []
    while True:
        print("Write the name of the item that you want to put. If that is enough, write 'quit'.")
        item = input()
        if item == 'quit':
            print("Items in your list: ")
            for i in liste:
                print(i)
            break
        liste.append(item)
    return liste

def closest_match(word, word_list):
    if word in word_list:
        return word
    min_dist = float('inf')
    closest_word = ''

    for i in word_list:
        # Convert to strings before calculating edit distance
        i_str = str(i)
        word_str = str(word)

        dist = editdistance.eval(word_str, i_str)

        if dist < min_dist:
            min_dist = dist
            closest_word = i_str

    return closest_word

def closest_match_list(liste, word_list):
    new_list = []
    for i in liste:
        new_list.append(closest_match(i, word_list))
    return new_list