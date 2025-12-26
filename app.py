import streamlit as st
import pandas as pd
import requests  # <--- THIS WAS MISSING

st.set_page_config(page_title="AI Movie Recommender", layout="wide")

st.title("🎬 Premium Movie Recommender")
st.markdown("---")

@st.cache_data
def load_data():
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

# Function to fetch poster
def get_poster(movie_title):
    api_key = "6cc445b8"
    # We add .replace(' ', '+') to make the title URL-friendly
    url = f"http://www.omdbapi.com/?t={movie_title.replace(' ', '+')}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if 'Poster' in data and data['Poster'] != "N/A":
            return data['Poster']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Found"
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error"

# 2. The Visual Gallery
cols = st.columns(5)
recommended_list = recommendations[recommendations['Movie_Title'] != selected_movie].head(5)

for i, (index, row) in enumerate(recommended_list.iterrows()):
    with cols[i]:
        poster_url = get_poster(row['Movie_Title'])
        st.image(poster_url, use_container_width=True)
        st.write(f"**{row['Movie_Title']}**")
