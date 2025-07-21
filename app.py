import streamlit as st
import pickle 
import pandas as pd
import requests
import time
import os

# Create a directory to cache posters
if not os.path.exists("poster_cache"):
    os.makedirs("poster_cache")

# Function to fetch movie poster using TMDb API with caching
def fetch_poster(movie_id, retries=5, delay=3):
    cache_file = f"poster_cache/{movie_id}.txt"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return f.read().strip()

    api_key = "45364a02607888489c6386324d19c"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            print(f"Attempt {attempt+1}: Status {response.status_code} for Movie ID {movie_id}")
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    full_poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                    with open(cache_file, "w") as f:
                        f.write(full_poster_url)
                    return full_poster_url
                return "https://via.placeholder.com/500x750?text=No+Poster"
            elif response.status_code == 401:
                print("Invalid API Key")
                return "https://via.placeholder.com/500x750?text=Invalid+API+Key"
            elif response.status_code == 429:
                print("Rate limit hit, waiting...")
                time.sleep(10)
            else:
                print(f"Unexpected status: {response.status_code}")
                time.sleep(delay)
        except requests.RequestException as e:
            print(f"Error: {e}, retrying in {delay}s...")
            time.sleep(delay)
    return "https://via.placeholder.com/500x750?text=Failed+After+Retries"

# Load the dictionary and similarity matrix
try:
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading pickle files: {str(e)}")
    st.stop()

# Convert dictionary back to DataFrame
movies = pd.DataFrame(movies_dict)

# Check if 'id' column exists
if 'id' not in movies.columns:
    st.error("Error: 'id' column not found in the DataFrame. Please update the dataset.")
    st.stop()

# Streamlit app
st.title("Movie Recommender System")

# Test image to check if Streamlit can display images
st.write("Testing image display with a sample URL:")
test_image_url = "https://via.placeholder.com/500x750?text=Test+Image"
try:
    st.image(test_image_url, width=500)
except Exception as e:
    st.error(f"Error displaying test image: {str(e)}")

# Dropdown for selecting a movie
selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

# Recommend function
def recommend(movie):
    matching_movies = movies[movies['title'] == movie]
    if len(matching_movies) == 0:
        return ["Movie not found in the database!"], []
    
    movie_index = matching_movies.index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:3]
    
    recommended_movies = []
    recommended_posters = []
    
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]]['id']
        poster_url = fetch_poster(movie_id)
        recommended_posters.append(poster_url)
        time.sleep(2)
    
    return recommended_movies, recommended_posters

# Show recommendations when the button is clicked
if st.button('Recommend'):
    st.write('You selected:', selected_movie_name)
    
    with st.spinner('Fetching recommendations...'):
        recommendations, posters = recommend(selected_movie_name)
    
    st.write("Recommended Movies:")
    
    # Check if all posters are placeholders
    all_placeholders = all("via.placeholder.com" in p for p in posters)
    
    if all_placeholders:
        st.warning("If posters are not loading, it might be due to a network issue. Please ensure a stable internet connection.")
    
    # Use columns with adjusted layout
    cols = st.columns(3)
    for idx, (movie, poster) in enumerate(zip(recommendations, posters)):
        with cols[idx % 3]:
            st.text(movie)  # Display movie title
            st.write("")   # Add a blank line for spacing
            try:
                st.image(poster, width=300)  # Removed height parameter
            except Exception as e:
                st.error(f"Error displaying image for {movie}: {str(e)}")
                st.image("https://via.placeholder.com/300x450?text=Image+Not+Available", width=300)