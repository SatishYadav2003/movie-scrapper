import json

# Load the JSON file
with open("compiled_movie_details.json", "r", encoding="utf-8") as file:
    movie_details = json.load(file)

# Add movie_id to all movies
for movie in movie_details:
    download_link = movie["download_page_link"]
    movie["movie_id"] = download_link.split("/")[-1].split(".")[0]  # Extract unique ID

# Save the updated JSON back
with open("compiled_movie_details.json", "w", encoding="utf-8") as file:
    json.dump(movie_details, file, ensure_ascii=False, indent=4)

print("✅ All movie IDs added successfully!")
