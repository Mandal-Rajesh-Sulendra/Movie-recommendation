# app.py
import streamlit as st
from preprocessing import load_and_preprocess
from recommendation import build_model, recommend

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Movie Recommendation System")
st.write("Get the Top 5 similar movies based on content features.")

# Cache the dataset loading and model building for high performance
@st.cache_resource
def load_all_data():
    df = load_and_preprocess()
    similarity = build_model(df)
    return df, similarity

try:
    df, similarity = load_all_data()
    
    # Input field and search button
    movie_input = st.text_input("Enter movie name:", placeholder="e.g. Avatar, Inception...")
    
    if st.button("Recommend"):
        if movie_input.strip() == "":
            st.warning("Please enter a movie title.")
        else:
            recs, suggestions = recommend(movie_input, df, similarity)
            
            if recs:
                st.subheader(f"Top 5 Recommendations for '{movie_input}':")
                for i, title in enumerate(recs, 1):
                    st.write(f"**{i}. {title}**")
            else:
                st.error(f"Movie '{movie_input}' not found in the dataset.")
                if suggestions:
                    st.info(f"Did you mean: {', '.join(suggestions)}?")

except Exception as e:
    st.error("Error loading dataset. Please check if the TMDB CSV files are in the same folder.")
    st.exception(e)
