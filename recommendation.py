# recommendation.py
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_model(df):
    """Vectorize tags and compute cosine similarity matrix."""
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return similarity

def recommend(movie_name, df, similarity):
    """Find Top 5 similar movies. Returns (recommendations_list, suggestions_list)."""
    movie_name = movie_name.strip().lower()
    titles = df['title'].str.lower().tolist()

    if movie_name not in titles:
        suggestions = [t for t in df['title'].tolist() if movie_name in t.lower()][:3]
        return None, suggestions

    idx = titles.index(movie_name)
    scores = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)
    
    recs = [df.iloc[movie_idx]['title'] for movie_idx, _ in scores[1:6]]
    return recs, []
