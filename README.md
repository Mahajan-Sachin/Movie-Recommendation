# 🎬 Movie Recommender System

A movie recommendation system built using Python, Streamlit, and the TMDb API, leveraging NLP techniques like vectorization and NLTK for text preprocessing.
It recommends movies based on cosine similarity of features (genres, overview, cast, etc.) and displays posters using the TMDb API.

----
<img width="1121" height="859" alt="image" src="https://github.com/user-attachments/assets/b69f64a6-bfef-4d2c-8c7e-ebe984869edb" />

-----
<img width="1170" height="848" alt="image" src="https://github.com/user-attachments/assets/86a8e7fc-673a-4714-b244-6fe0839ffc55" />

## 📌 Features

🎯 Select a movie from a dropdown and get personalized recommendations.

🖼️ Fetches movie posters using the TMDb API.

🧠 Uses NLP techniques (vectorization, NLTK) for text preprocessing and similarity computation.

⚡ Optimized with caching to reduce API call times.

---

## 📂 Dataset
This project uses the TMDb Movie Metadata dataset, which contains data for 5000+ movies including genres, overviews, and cast.

📥 Download the dataset from Kaggle → TMDb Movie Metadata(https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

---

## ⚙️ Setup Instructions
Follow these steps to set up and run the project locally:

1️⃣ Install Dependencies
Install required libraries using pip:

pip install streamlit pandas requests numpy scikit-learn nltk
2️⃣ Generate similarity.pkl
⚠️ The similarity.pkl file is not included due to GitHub’s file size limits.

Steps:

1). Open movie_reco.ipynb or movie_recommender.ipynb in Jupyter Notebook.

2). Run the notebook to:

3). Preprocess the data

4). Compute the cosine similarity matrix

Generate similarity.pkl and possibly movie_dict.pkl or other .pkl files

3️⃣ Run the App
streamlit run app.py
Then open the URL shown in the terminal (usually http://localhost:8501) in your browser.

🎥 Select a movie → Click "Recommend" → View movie recommendations with posters!

---

## ⚠️ Notes
Ensure a stable internet connection to fetch movie posters using the TMDb API.

The app uses a TMDb API key (already included in the code). If it expires, get a new one from TMDb and update it in app.py.

---

## 🚧 Future Work
🌍 Deployment: Plan to deploy on Streamlit Community Cloud.

💅 UI Enhancements: Add genre-based filtering and better UI.

⚙️ Performance: Optimize similarity calculations for large datasets.

---

## 🧰 Tech Stack
Languages & Libraries: Python, Streamlit, Pandas, NumPy, Scikit-learn, NLTK

API: TMDb API

Techniques: NLP (Vectorization, Text Preprocessing), Cosine Similarity

---
🤝 Contributing
Feel free to fork the repository, suggest improvements, or open a pull request.
Feedback and suggestions are always welcome in the issues section!
