import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from sklearn.feature_extraction.text import CountVectorizer


# -----------------------------
# TMDB API KEY
# -----------------------------

API_KEY = "e3c659b5a1c10abb58839dddee76ac03"


# -----------------------------
# Load Dataset and Create Vectors
# -----------------------------

@st.cache_data
def load_data():

    movies = pd.read_csv("processed_movies.csv")

    cv = CountVectorizer(
        max_features=5000,
        stop_words="english"
    )

    vectors = cv.fit_transform(
        movies["tags"]
    ).toarray()

    return movies, vectors


movies, vectors = load_data()



# -----------------------------
# Fetch Movie Poster
# -----------------------------

def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Poster"


    data = response.json()

    poster_path = data.get("poster_path")


    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path


    return "https://via.placeholder.com/500x750?text=No+Poster"


# -----------------------------
# Recommendation Function
# -----------------------------

def recommend(movie_name):

    if movie_name not in movies["title"].values:
        return []


    movie_index = movies[
        movies["title"] == movie_name
    ].index[0]


    selected_vector = vectors[movie_index]


    similarity_scores = []


    for i in range(len(vectors)):

        movie_vector = vectors[i]


        dot_product = np.dot(
            selected_vector,
            movie_vector
        )


        magnitude1 = np.linalg.norm(
            selected_vector
        )

        magnitude2 = np.linalg.norm(
            movie_vector
        )


        if magnitude1 == 0 or magnitude2 == 0:
            similarity = 0

        else:
            similarity = (
                dot_product /
                (magnitude1 * magnitude2)
            )


        similarity_scores.append(
            (i, similarity)
        )



    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )


    recommended_movies = []

    count = 0


    for movie in similarity_scores:


        if movie[0] != movie_index:


            recommended_movies.append({

                "movie_id":
                movies.iloc[movie[0]].movie_id,


                "title":
                movies.iloc[movie[0]].title,


                "similarity":
                round(movie[1] * 100, 2)

            })


            count += 1



        if count == 5:
            break



    return recommended_movies




# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="Movie Recommendation Engine",
    page_icon="🎬",
    layout="wide"
)



st.title(
    "🎬 Content-Based Movie Recommendation Engine"
)


st.markdown(
    """
    Find movies similar to your favorite movie using
    **Content-Based Filtering**.
    """
)



# Sidebar

with st.sidebar:

    st.header("📌 About")


    st.write(
        """
        This project uses:

        ✅ Pandas  
        ✅ NumPy  
        ✅ Plotly  
        ✅ Streamlit  

        Dataset:
        TMDB 5000 Movies
        """
    )


    st.divider()


    st.caption(
        "Built using Python"
    )



st.divider()



# Movie Selection

col1, col2, col3 = st.columns(
    [1,2,1]
)


with col2:


    selected_movie = st.selectbox(
        "🎥 Select a Movie",
        movies["title"].values
    )


    recommend_button = st.button(
        "✨ Recommend Movies"
    )




# Recommendation Output

if recommend_button:


    results = recommend(
        selected_movie
    )


    st.success(
        "Top 5 Recommendations Found!"
    )


    st.subheader(
        "🎬 Recommended Movies"
    )


    movie_names = []

    similarity_values = []


    cols = st.columns(5)



    for i, movie in enumerate(results):


        with cols[i]:


            poster = fetch_poster(
                movie["movie_id"]
            )


            if poster:

                st.image(
                    poster,
                    use_container_width=True
                )


            else:

                st.write(
                    "🎬 No Poster"
                )


            st.markdown(
                f"**{movie['title']}**"
            )


            st.caption(
                f"⭐ Similarity: {movie['similarity']}%"
            )


            movie_names.append(
                movie["title"]
            )


            similarity_values.append(
                movie["similarity"]
            )




    # Plotly Chart

    fig = px.bar(

        x=similarity_values,

        y=movie_names,

        orientation="h",

        text=similarity_values,

        labels={

            "x": "Similarity (%)",

            "y": "Movie Title"

        },

        title="Top 5 Similar Movies"

    )



    fig.update_layout(

        template="plotly_dark",

        height=500,

        showlegend=False,

        yaxis={
            "categoryorder":
            "total ascending"
        }

    )



    st.plotly_chart(
        fig,
        use_container_width=True
    )