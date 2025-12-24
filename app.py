import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Pro AI Recommender", layout="wide")
st.title("🚀 Advanced AI Movie Engine")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/YBI-Foundation/Dataset/main/Movies%20Recommendation.csv"
    df = pd.read_csv(url)
    # Fill any empty descriptions to avoid errors
    df['Movie_Genre'] = df['Movie_Genre'].fillna('')
    return df

df = load_data()

# --- THE AI PART ---
# This converts movie genres into numbers so the computer can 'calculate' similarity
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Movie_Genre'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
# --------------------

selected_movie = st.sidebar.selectbox("Select a movie:", df['Movie_Title'].unique())

def get_recommendations(title):
    idx = df[df['Movie_Title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    movie_indices = [i[0] for i in sim_scores[1:6]]
    return df.iloc[movie_indices]

st.subheader(f"AI suggests these based on '{selected_movie}':")
recs = get_recommendations(selected_movie)

cols = st.columns(5)
for i, (index, row) in enumerate(recs.iterrows()):
    with cols[i]:
        st.image("https://via.placeholder.com/500x750?text=Movie", use_container_width=True)
        st.write(f"**{row['Movie_Title']}**")
        st.caption(f"Match Score: {round(row['Movie_Popularity']/10, 1)}/10")
