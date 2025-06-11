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
    # Check if poster is already cached
    cache_file = f"poster_cache/{movie_id}.txt"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cached_url = f.read().strip()
            print(f"Poster URL for Movie ID {movie_id} loaded from cache: {cached_url}")
            return cached_url

    api_key = "fc06cf98a163206388def73a8995bd3a"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            print(f"Request URL: {url}")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 404:
                print(f"Movie ID {movie_id} not found in TMDb database.")
                return "https://via.placeholder.com/500x750?text=Movie+Not+Found"
            
            if response.status_code == 401:
                print("Error: Invalid API Key. Please check your TMDb API key.")
                return "https://via.placeholder.com/500x750?text=Invalid+API+Key"
            
            if response.status_code == 429:
                print("Error: Too many requests. TMDb API rate limit exceeded. Waiting...")
                time.sleep(10)
                continue
            
            response.raise_for_status()
            data = response.json()
            print(f"Response Data for Movie ID {movie_id}: {data}")
            
            poster_path = data.get('poster_path')
            if poster_path:
                full_poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                print(f"Poster URL for Movie ID {movie_id}: {full_poster_url}")
                # Cache the poster URL
                with open(cache_file, "w") as f:
                    f.write(full_poster_url)
                return full_poster_url
            else:
                print(f"No poster available for Movie ID {movie_id}.")
                return "https://via.placeholder.com/500x750?text=No+Poster+Available"
                
        except requests.exceptions.Timeout:
            print(f"Timeout error for Movie ID {movie_id}. Retrying ({attempt+1}/{retries})...")
            time.sleep(delay)
            continue
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error for Movie ID {movie_id}: {str(e)}. Retrying ({attempt+1}/{retries})...")
            time.sleep(delay)
            continue
        except Exception as e:
            print(f"Error fetching poster for Movie ID {movie_id}: {str(e)}")
            return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"
    
    print(f"Failed to fetch poster for Movie ID {movie_id} after {retries} retries.")
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
    st.image(test_image_url, use_column_width=True)
except Exception as e:
    st.error(f"Error displaying test image: {str(e)}")

# Network stability warning
st.warning("If posters are not loading, it might be due to a network issue. Please ensure a stable internet connection.")

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
    # Take top 3 movies including the selected movie (index 0)
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:3]
    
    recommended_movies = []
    recommended_posters = []
    
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]]['id']
        poster_url = fetch_poster(movie_id)
        recommended_posters.append(poster_url)
        time.sleep(2)  # Reduced delay to optimize speed
    
    return recommended_movies, recommended_posters

# Show recommendations when the button is clicked
if st.button('Recommend'):
    st.write('You selected:', selected_movie_name)
    
    with st.spinner('Fetching recommendations...'):
        recommendations, posters = recommend(selected_movie_name)
    
    st.write("Recommended Movies:")
    
    cols = st.columns(3)
    for idx, (movie, poster) in enumerate(zip(recommendations, posters)):
        col = cols[idx % 3]
        with col:
            st.text(movie)
            try:
                st.image(poster, use_column_width=True)
            except Exception as e:
                st.error(f"Error displaying image for {movie}: {str(e)}")
                st.image("https://via.placeholder.com/500x750?text=Image+Not+Available", use_column_width=True)