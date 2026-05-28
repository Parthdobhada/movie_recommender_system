import streamlit as st
import pickle
import pandas as pd
import requests

# Page Config
st.set_page_config(
    page_title="Movie Recommender",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
</style>
""", unsafe_allow_html=True)

# OMDb API Key
API_KEY = st.secrets["API_KEY"]

# Fetch Movie Details
@st.cache_data
def fetch_details(movie_name):

    url = f"https://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    response = requests.get(url)

    data = response.json()

    if data.get("Response") == "True":

        poster = data.get("Poster")

        if poster == "N/A":
            poster = "https://via.placeholder.com/300x450?text=No+Poster"

        return {
            "poster": poster,
            "rating": data.get("imdbRating", "N/A"),
            "genre": data.get("Genre", "N/A"),
            "year": data.get("Year", "N/A"),
            "plot": data.get("Plot", "N/A")
        }

    return {
        "poster": "https://via.placeholder.com/300x450?text=No+Poster",
        "rating": "N/A",
        "genre": "N/A",
        "year": "N/A",
        "plot": "N/A"
    }


# Recommend Function
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_scores = []
    recommended_ratings = []
    recommended_genres = []
    recommended_years = []

    for i in movies_list:

        movie_title = movies.iloc[i[0]].title

        details = fetch_details(movie_title)

        recommended_movies.append(movie_title)

        recommended_posters.append(details['poster'])

        recommended_scores.append(round(i[1] * 100, 2))

        recommended_ratings.append(details['rating'])

        recommended_genres.append(details['genre'])

        recommended_years.append(details['year'])

    return (
        recommended_movies,
        recommended_posters,
        recommended_scores,
        recommended_ratings,
        recommended_genres,
        recommended_years
    )


# Load Data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

import gzip

with gzip.open('similarity_compressed.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)


# UI
st.title("🎬 Movie Recommender System")

st.subheader("Find Similar Movies")

selected_movie_name = st.selectbox(
    "Select a Movie",
    movies['title'].values
)


# Recommend Button
if st.button('Recommend'):

    with st.spinner('Finding best movies for you...'):

        (
            names,
            posters,
            scores,
            ratings,
            genres,
            years
        ) = recommend(selected_movie_name)

        st.subheader(f"Because you watched {selected_movie_name}")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.image(posters[0])
            st.text(names[0])
            st.write(f"⭐ IMDb: {ratings[0]}")
            st.write(f"🎭 {genres[0]}")
            st.write(f"📅 {years[0]}")
            st.write(f"📊 Similarity: {scores[0]}%")

        with col2:
            st.image(posters[1])
            st.text(names[1])
            st.write(f"⭐ IMDb: {ratings[1]}")
            st.write(f"🎭 {genres[1]}")
            st.write(f"📅 {years[1]}")
            st.write(f"📊 Similarity: {scores[1]}%")

        with col3:
            st.image(posters[2])
            st.text(names[2])
            st.write(f"⭐ IMDb: {ratings[2]}")
            st.write(f"🎭 {genres[2]}")
            st.write(f"📅 {years[2]}")
            st.write(f"📊 Similarity: {scores[2]}%")

        with col4:
            st.image(posters[3])
            st.text(names[3])
            st.write(f"⭐ IMDb: {ratings[3]}")
            st.write(f"🎭 {genres[3]}")
            st.write(f"📅 {years[3]}")
            st.write(f"📊 Similarity: {scores[3]}%")

        with col5:
            st.image(posters[4])
            st.text(names[4])
            st.write(f"⭐ IMDb: {ratings[4]}")
            st.write(f"🎭 {genres[4]}")
            st.write(f"📅 {years[4]}")
            st.write(f"📊 Similarity: {scores[4]}%")