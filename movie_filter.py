import json
import re


adult_categories_substrings = [
    "hot web series",
    "latest hindi short films",
    "altbalaji web series",
    "moodx web series",
    "hulchul web series",
    "japanese movies",
    "tagalog movies",
    "bullapp hot web series",
    "ullu web series",
    "atrangii web series",
    "boomex web series",
    "neonx"
]


movie_name_18_plus_pattern = re.compile(
    r"^\s*[\(\[]?\s*18\s*[\+\%\s]*\s*[\)\]]?", re.IGNORECASE
)

def contains_adult_category(category_text):
    if not category_text:
        return False
    category_text = category_text.lower()
    for substr in adult_categories_substrings:
        if substr in category_text:
            return True
    return False

def starts_with_18_plus(movie_name):
    if not movie_name:
        return False
    return bool(movie_name_18_plus_pattern.match(movie_name))

def contains_primeplay(movie_name):
    if not movie_name:
        return False
    return "primeplay" in movie_name.lower()

def filter_adult_movies(input_json_path, output_json_path):
    with open(input_json_path, 'r', encoding='utf-8') as f:
        movies = json.load(f)

    filtered_movies = []
    filtered_out_movies = []

    for movie in movies:
        name = movie.get("Movie Name", "")
        category = movie.get("Movie Category", "")

        if (
            contains_adult_category(category)
            or starts_with_18_plus(name)
            or contains_primeplay(name)
        ):
            filtered_out_movies.append(movie)
        else:
            filtered_movies.append(movie)

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_movies, f, indent=4, ensure_ascii=False)

    # Reporting
    print("----- Filtered OUT Adult Movies -----")
    if filtered_out_movies:
        for m in filtered_out_movies:
            print(f" - {m.get('Movie Name')} | Category: {m.get('Movie Category')}")
    else:
        print("No adult movies found.")

    print("\n----- Movies Passed Filtering -----")
    for m in filtered_movies:
        print(f" - {m.get('Movie Name')} | Category: {m.get('Movie Category')}")

    print(f"\nSummary:")
    print(f"Total movies in input: {len(movies)}")
    print(f"Filtered out adult movies: {len(filtered_out_movies)}")
    print(f"Movies after filtering: {len(filtered_movies)}")
    print(f"Filtered list saved to {output_json_path}")

# Usage
input_json = "compiled_movie_details.json"
output_json = "movies_filtered.json"

filter_adult_movies(input_json, output_json)
