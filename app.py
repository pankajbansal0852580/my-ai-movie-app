import streamlit as st
import pandas as pd
import requests  # <--- THIS WAS MISSING

# --- THEME STYLING ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* Making the text white to stand out against the dark background */
    h1, h2, h3, p, .stMarkdown {{
        color: white !important;
    }}

    /* Styling the Sidebar to look modern */
    [data-testid="stSidebar"] {{
        background-color: rgba(20, 20, 20, 0.8);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="AI Movie Recommender", layout="wide")

st.title("🎬Movie Recommender")
st.markdown("---")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/YBI-Foundation/Dataset/main/Movies%20Recommendation.csv"
    data = pd.read_csv(url)
    return data

df = load_data()

# --- Updated Search with 'The Avengers' as Default ---
st.sidebar.title("🔍 Search Movies")

# 1. Find the position (index) of Avengers in our list
# Note: Ensure the name matches exactly how it appears in your CSV
try:
    default_index = df[df['Movie_Title'] == 'The Godfather'].index[0]
    # We convert the absolute index to the position in the unique list
    list_index = list(df['Movie_Title'].unique()).index('The Godfather')
except:
    list_index = 0 # Fallback to first movie if not found

selected_movie = st.sidebar.selectbox(
    "Type a movie title:",
    options=df['Movie_Title'].unique(),
    index=list_index, # This sets the default!
    placeholder="Start typing...",
    help="Type the name of a movie you've watched recently!"
)
# --- Add a 'Reset' button (Optional but Pro) ---
if st.sidebar.button("Clear Selection"):
    st.rerun()

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
        
        # This creates a Google Search link for the movie
        search_url = f"https://www.google.com/search?q={row['Movie_Title'].replace(' ', '+')}+movie"
        
        # We use st.markdown with 'unsafe_allow_html' to make the image clickable
        st.markdown(
            f'''
            <a href="{search_url}" target="_blank">
                <img src="{poster_url}" style="width:100%; border-radius: 10px; transition: 0.3s;" 
                     onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'">
            </a>
            ''',
            unsafe_allow_html=True
        )
        st.write(f"**{row['Movie_Title']}**")
