import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer

movies = pd.read_csv("processed_movies.csv")

print("Dataset Loaded Successfully!")

cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(movies["tags"]).toarray()

print("Vectors Created Successfully!")


# Recommendation Function


def recommend(movie_name):

    if movie_name not in movies["title"].values:
        print("Movie not found!")
        return

    movie_index = movies[movies["title"] == movie_name].index[0]

    selected_vector = vectors[movie_index]

    similarity_scores = []

    # Calculate similarity with every movie
    for i in range(len(vectors)):

        movie_vector = vectors[i]

        # Dot Product
        dot_product = np.dot(selected_vector, movie_vector)

        # Magnitude
        magnitude1 = np.linalg.norm(selected_vector)
        magnitude2 = np.linalg.norm(movie_vector)

        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            similarity = 0
        else:
            similarity = dot_product / (magnitude1 * magnitude2)

        similarity_scores.append((i, similarity))

    # Sort by similarity
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    print("\nTop 5 Recommended Movies\n")

    count = 0

    for movie in similarity_scores:

        if movie[0] != movie_index:

            print(
                movies.iloc[movie[0]].title,
                "-",
                round(movie[1] * 100, 2),
                "%"
            )

            count += 1

        if count == 5:
            break



# User Input


movie_name = input("Enter Movie Name: ")

recommend(movie_name)