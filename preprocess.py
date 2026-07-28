import pandas as pd
import ast

# Load datasets
movies = pd.read_csv("dataset/tmdb_5000_movies.csv")
credits = pd.read_csv("dataset/tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on="title")

# Keep required columns
movies = movies[
    [
        "movie_id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew"
    ]
]

# Remove missing values
movies.dropna(inplace=True)


# ---------- FUNCTIONS ----------

# Extract names from genres and keywords
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i["name"])
    return L


# Extract top 3 cast members
def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter != 3:
            L.append(i["name"])
            counter += 1
        else:
            break
    return L


# Extract director
def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i["job"] == "Director":
            L.append(i["name"])
            break
    return L


# ---------- APPLY FUNCTIONS ----------

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert3)
movies["crew"] = movies["crew"].apply(fetch_director)

# Convert overview into list
movies["overview"] = movies["overview"].apply(lambda x: x.split())

# Remove spaces from names
movies["genres"] = movies["genres"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["keywords"] = movies["keywords"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["cast"] = movies["cast"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["crew"] = movies["crew"].apply(lambda x: [i.replace(" ", "") for i in x])

# Create tags column
movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

# Keep only useful columns
new_df = movies[["movie_id", "title", "tags"]]

# Convert tags list into a single string
new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))

# Convert to lowercase
new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())

print(new_df.head())

# Save the processed dataset
new_df.to_csv("processed_movies.csv", index=False)

print("\nPreprocessing completed successfully!")
print("processed_movies.csv has been created.")