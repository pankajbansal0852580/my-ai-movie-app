import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Movie Recommender", layout="wide")

st.title("🎬 Premium Movie Recommender")
st.markdown("---")

@st.cache_data
def load_data():
    # Using the same reliable dataset
    url = "https://raw.githubusercontent.com/YBI-Foundation/Dataset/main/Movies%20Recommendation.csv"
    data = pd.read_csv(url)
    return data

df = load_data()

# Sidebar Setup
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2503/2503508.png", width=100)
st.sidebar.title("Settings")
selected_movie = st.sidebar.selectbox("Type or select a movie:", df['Movie_Title'].unique())

# Logic: Find the Genre and Recommendations
movie_row = df[df['Movie_Title'] == selected_movie].iloc[0]
genre = movie_row['Movie_Genre']
recommendations = df[df['Movie_Genre'] == genre].head(6)

st.subheader(f"Because you liked '{selected_movie}'")
st.caption(f"Category: {genre}")

# 2. The Visual Gallery
cols = st.columns(5)

# We loop through the recommendations (skipping the one already selected)
recommended_list = recommendations[recommendations['Movie_Title'] != selected_movie].head(5)

for i, (index, row) in enumerate(recommended_list.iterrows()):
    with cols[i]:
        # Placeholder for now
        poster_url = "https://via.placeholder.com/500x750?text=Movie"
        
        st.image(poster_url, use_container_width=True)
        st.write(f"**{row['Movie_Title']}**")
        
        # We changed 'Movie_Rating' to 'Movie_Genre' or 'Movie_Language' to avoid the error
        st.caption(f"Language: {row['Movie_Language']}")