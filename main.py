# main.py — Movie Recommendation System
# Roll No: CSE003 & CSE049 | CSE Mini Project | 2024-2025
# Run: python main.py

import os, sys
from preprocessing  import load_and_preprocess
from recommendation import build_model, recommend

# Check dataset files exist
for f in ["tmdb_5000_movies.csv", "tmdb_5000_credits.csv"]:
    if not os.path.isfile(f):
        print(f"ERROR: '{f}' not found.")
        print("Download from: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata")
        sys.exit()

print("Loading data...")
df = load_and_preprocess()

print("Building model...")
similarity = build_model(df)
print(f"Done. {len(df)} movies loaded.\n")

# Interactive loop
while True:
    movie = input("Enter movie name (or 'quit' to exit): ").strip()
    if movie.lower() in ('quit', 'exit', ''):
        break
    
    recs, suggestions = recommend(movie, df, similarity)
    if recs:
        print("\nTop 5 Recommended Movies:")
        for i, title in enumerate(recs, 1):
            print(f"{i}. {title}")
    else:
        print(f"Movie '{movie}' not found in dataset.")
        if suggestions:
            print(f"Did you mean: {suggestions}")
