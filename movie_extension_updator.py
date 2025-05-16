import json
import re

def update_urls(json_data):
    for movie in json_data:
        for key, value in movie.items():
            if isinstance(value, str) and "https://www.mp4moviez." in value:
                movie[key] = re.sub(r"https://www\.mp4moviez\.[a-zA-Z0-9]+", "https://www.mp4moviez.law", value)
    return json_data



with open("compiled_movie_details.json", "r", encoding="utf-8") as file:
    data = json.load(file)


data = update_urls(data)


with open("compiled_movie_details.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("URLs updated successfully!")
