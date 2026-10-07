"""
Movie / Netflix Dataset Analyzer
---------------------------------
A micro-project that loads a Netflix-style catalogue dataset, cleans it,
and produces summary statistics and visualisations describing the content
library (movies vs TV shows, genres, countries, ratings, release trends,
and movie duration).

Author : Hani Ashwinbhai Dharsandiya
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# 1. Load Dataset
# ---------------------------------------------------------------------
df = pd.read_csv("netflix_titles.csv")
print("Dataset shape (rows, columns):", df.shape)
print("\nColumn names:\n", list(df.columns))
print("\nFirst 5 records:\n", df.head())

# ---------------------------------------------------------------------
# 2. Data Cleaning
# ---------------------------------------------------------------------
print("\nMissing values per column:\n", df.isnull().sum())

df["director"] = df["director"].fillna("Not Specified")
df["country"] = df["country"].fillna("Unknown")
df.drop_duplicates(subset="show_id", inplace=True)

# ---------------------------------------------------------------------
# 3. Basic Analysis
# ---------------------------------------------------------------------
type_counts = df["type"].value_counts()
print("\nContent type distribution:\n", type_counts)

top_countries = df["country"].value_counts().head(10)
print("\nTop 10 countries by number of titles:\n", top_countries)

# Split multi-genre 'listed_in' field and count individual genres
genre_series = df["listed_in"].str.split(", ").explode()
top_genres = genre_series.value_counts().head(10)
print("\nTop 10 genres:\n", top_genres)

rating_counts = df["rating"].value_counts()
print("\nContent rating distribution:\n", rating_counts)

titles_per_year = df["release_year"].value_counts().sort_index()

movie_durations = (
    df[df["type"] == "Movie"]["duration"]
    .str.replace(" min", "", regex=False)
    .astype(int)
)
print("\nAverage movie duration (minutes):", round(movie_durations.mean(), 1))
print("Shortest movie:", movie_durations.min(), "min | Longest movie:", movie_durations.max(), "min")

# ---------------------------------------------------------------------
# 4. Visualisations
# ---------------------------------------------------------------------

# 4.1 Movies vs TV Shows
plt.figure(figsize=(5, 5))
plt.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%",
        colors=["#E50914", "#221f1f"], startangle=90,
        textprops={"color": "white"})
plt.title("Movies vs TV Shows")
plt.savefig("chart_type_distribution.png", bbox_inches="tight", dpi=150)
plt.close()

# 4.2 Top 10 Countries
plt.figure(figsize=(8, 5))
top_countries.sort_values().plot(kind="barh", color="#E50914")
plt.title("Top 10 Countries by Number of Titles")
plt.xlabel("Number of Titles")
plt.tight_layout()
plt.savefig("chart_top_countries.png", dpi=150)
plt.close()

# 4.3 Top 10 Genres
plt.figure(figsize=(8, 5))
top_genres.sort_values().plot(kind="barh", color="#221f1f")
plt.title("Top 10 Genres")
plt.xlabel("Number of Titles")
plt.tight_layout()
plt.savefig("chart_top_genres.png", dpi=150)
plt.close()

# 4.4 Titles added over release years
plt.figure(figsize=(9, 5))
titles_per_year.plot(kind="line", marker="o", color="#E50914")
plt.title("Number of Titles by Release Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("chart_titles_per_year.png", dpi=150)
plt.close()

# 4.5 Content Rating distribution
plt.figure(figsize=(8, 5))
rating_counts.plot(kind="bar", color="#E50914")
plt.title("Content Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart_rating_distribution.png", dpi=150)
plt.close()

# 4.6 Movie duration histogram
plt.figure(figsize=(8, 5))
plt.hist(movie_durations, bins=20, color="#221f1f", edgecolor="white")
plt.title("Distribution of Movie Durations")
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of Movies")
plt.tight_layout()
plt.savefig("chart_movie_durations.png", dpi=150)
plt.close()

print("\nAll charts saved successfully as PNG files.")

# ---------------------------------------------------------------------
# 5. Export summary report
# ---------------------------------------------------------------------
with open("summary_report.txt", "w") as f:
    f.write("MOVIE / NETFLIX DATASET ANALYZER - SUMMARY REPORT\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Total titles analysed : {len(df)}\n\n")
    f.write("Content type distribution:\n")
    f.write(type_counts.to_string() + "\n\n")
    f.write("Top 10 countries:\n")
    f.write(top_countries.to_string() + "\n\n")
    f.write("Top 10 genres:\n")
    f.write(top_genres.to_string() + "\n\n")
    f.write("Content rating distribution:\n")
    f.write(rating_counts.to_string() + "\n\n")
    f.write(f"Average movie duration: {round(movie_durations.mean(),1)} minutes\n")

print("Summary report written to summary_report.txt")
