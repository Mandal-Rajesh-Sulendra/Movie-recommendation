# eda.py — Exploratory Data Analysis
import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# 1. Load Datasets
movies = pd.read_csv("tmdb_5000_movies.csv")

# Helper function to parse JSON-like columns
def parse_column(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)]
    except:
        return []

# 2. Chart 1: Top Movie Genres
all_genres = []
for item in movies['genres'].dropna():
    all_genres.extend(parse_column(item))

genre_counts = Counter(all_genres).most_common(10)
g_df = pd.DataFrame(genre_counts, columns=['Genre', 'Count'])

plt.figure(figsize=(10, 5))
sns.barplot(x='Count', y='Genre', data=g_df, palette='viridis')
plt.title('Top 10 Movie Genres')
plt.xlabel('Number of Movies')
plt.ylabel('Genre')
plt.tight_layout()
plt.savefig('genres_chart.png')
plt.close()

# 3. Chart 2: Highest Rated Movies (min 500 votes for fairness)
qualified = movies[movies['vote_count'] >= 500].nlargest(10, 'vote_average')
plt.figure(figsize=(10, 5))
sns.barplot(x='vote_average', y='title', data=qualified, palette='plasma')
plt.title('Top 10 Highest Rated Movies (min 500 votes)')
plt.xlabel('Average Rating')
plt.ylabel('Movie Title')
plt.xlim(7.5, 9.0)
plt.tight_layout()
plt.savefig('ratings_chart.png')
plt.close()

# 4. Chart 3: Most Common Keywords
all_keywords = []
for item in movies['keywords'].dropna():
    all_keywords.extend(parse_column(item))

keyword_counts = Counter(all_keywords).most_common(10)
k_df = pd.DataFrame(keyword_counts, columns=['Keyword', 'Count'])

plt.figure(figsize=(10, 5))
sns.barplot(x='Count', y='Keyword', data=k_df, palette='magma')
plt.title('Top 10 Most Common Keywords')
plt.xlabel('Frequency')
plt.ylabel('Keyword')
plt.tight_layout()
plt.savefig('keywords_chart.png')
plt.close()

# 5. Chart 4: Correlation Heatmap
cols = ['budget', 'popularity', 'revenue', 'runtime', 'vote_average', 'vote_count']
corr_matrix = movies[cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.savefig('heatmap_chart.png')
plt.close()

print("All 4 EDA charts generated and saved successfully!")
