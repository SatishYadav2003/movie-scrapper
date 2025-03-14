import shutil
import os
import subprocess

source_path = r"C:\Users\Satish Yadav\OneDrive\Desktop\Satish Coding\python program\New_Movie_Update_Scrapping\compiled_movie_details.json"
destination_path = r"C:\Users\Satish Yadav\OneDrive\Desktop\Satish Coding\MovieStore\Frontend\src\movielist\compiled_movie_details.json"

# source_path = os.path.join("..", "New_Movie_Update_Scrapping", "compiled_movie_details.json")
# destination_path = os.path.join("..", "MovieStore", "Frontend", "src", "movielist", "compiled_movie_details.json")


try:
    shutil.copy2(source_path, destination_path)
    print(f"\nSuccessfully copied to destination from source.\n")

    repo_path = r"C:\Users\Satish Yadav\OneDrive\Desktop\Satish Coding\MovieStore\Frontend"
    os.chdir(repo_path)

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "new movies added"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

    print("\nChanges pushed to GitHub successfully.\n")

except Exception as e:
    print(f"Error: {e}")
