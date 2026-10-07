"""
generate_dataset.py
Generates a synthetic Netflix-style catalogue dataset (netflix_titles.csv)
so the Movie/Netflix Dataset Analyzer has real data to work on.
"""
import random
import csv

random.seed(42)

types = ["Movie", "TV Show"]
countries = ["United States", "India", "United Kingdom", "Canada", "France",
             "Japan", "South Korea", "Germany", "Spain", "Australia", "Brazil"]
genres = ["Drama", "Comedy", "Action", "Documentary", "Thriller", "Romance",
          "Horror", "Sci-Fi", "Kids", "Anime", "Crime", "Reality-TV"]
ratings = ["G", "PG", "PG-13", "R", "TV-MA", "TV-14", "TV-PG", "TV-Y", "TV-Y7"]
directors = ["A. Sharma", "J. Miller", "K. Tanaka", "M. Rossi", "L. Dubois",
             "R. Kim", "S. Novak", "P. Silva", "T. Johnson", "N. Khan", None]
adjectives = ["Silent", "Broken", "Last", "Golden", "Hidden", "Dark", "Endless",
              "Lost", "Secret", "Final", "Crimson", "Distant", "Forgotten"]
nouns = ["Horizon", "Shadow", "Kingdom", "Journey", "City", "Legacy", "Dream",
         "River", "Storm", "Empire", "Garden", "Chronicles", "Signal"]

rows = []
show_id = 1
for _ in range(400):
    ttype = random.choices(types, weights=[0.68, 0.32])[0]
    title = f"{random.choice(adjectives)} {random.choice(nouns)}"
    if random.random() < 0.15:
        title += f" {random.choice(['II', 'III', ': Origins', ': Rebirth'])}"
    director = random.choice(directors) if ttype == "Movie" else (
        random.choice(directors) if random.random() < 0.3 else None)
    country = random.choice(countries)
    release_year = random.randint(1998, 2024)
    add_year = min(2024, release_year + random.randint(0, 4))
    date_added = f"{random.choice(['January','March','May','July','September','November'])} {random.randint(1,28)}, {add_year}"
    rating = random.choice(ratings)
    if ttype == "Movie":
        duration = f"{random.randint(70, 175)} min"
    else:
        duration = f"{random.randint(1, 9)} Season" + ("s" if random.randint(1,9) > 1 else "")
    n_genres = random.randint(1, 3)
    listed_in = ", ".join(random.sample(genres, n_genres))
    description = f"A {random.choice(['gripping','heartfelt','fast-paced','quirky','intense'])} story about {random.choice(['family','revenge','survival','love','ambition','friendship'])}."

    rows.append({
        "show_id": f"s{show_id}",
        "type": ttype,
        "title": title,
        "director": director if director else "",
        "country": country,
        "date_added": date_added,
        "release_year": release_year,
        "rating": rating,
        "duration": duration,
        "listed_in": listed_in,
        "description": description
    })
    show_id += 1

fieldnames = ["show_id", "type", "title", "director", "country", "date_added",
              "release_year", "rating", "duration", "listed_in", "description"]

with open("netflix_titles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> netflix_titles.csv")
