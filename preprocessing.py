# preprocessing.py
import pandas as pd
import ast

def get_names(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)]
    except:
        return []

def get_top3(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)[:3]]
    except:
        return []

def get_director(text):
    try:
        return [i['name'] for i in ast.literal_eval(text) if i['job'] == 'Director']
    except:
        return []

def load_and_preprocess():
    movies  = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")

    # Merge and select columns
    df = movies.merge(credits, on='title')
    df = df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']].dropna()

    # Parse JSON columns
    df['genres']   = df['genres'].apply(get_names)
    df['keywords'] = df['keywords'].apply(get_names)
    df['cast']     = df['cast'].apply(get_top3)
    df['crew']     = df['crew'].apply(get_director)
    df['overview'] = df['overview'].apply(lambda x: x.split())

    # Remove spaces so multi-word names become single tokens
    for col in ['genres', 'keywords', 'cast', 'crew']:
        df[col] = df[col].apply(lambda lst: [w.replace(" ", "") for w in lst])

    # Combine all into one tags string
    df['tags'] = df['overview'] + df['genres'] + df['keywords'] + df['cast'] + df['crew']
    df['tags'] = df['tags'].apply(lambda x: " ".join(x).lower())

    return df[['movie_id', 'title', 'tags']].reset_index(drop=True)
