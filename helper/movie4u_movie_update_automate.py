import shutil
import os
import subprocess
import sys

# Step 1: Run movie_filter.py
try:
    print("Running movie_filter.py...")
    subprocess.run([sys.executable, "movie_filter.py"], check=True)
    print("Filtering completed.\n")
except subprocess.CalledProcessError as e:
    print(f"Error while running movie_filter.py: {e}")
    sys.exit(1)


source_path = r"C:\Users\Satish Yadav\OneDrive\Desktop\Satish Coding\python program\New_Movie_Update_Scrapping\movies_filtered.json"
destination_path = r"C:\Users\Satish Yadav\OneDrive\Desktop\Satish Coding\MovieStore\Backend\compiled_movie_details.json"

try:
    shutil.copy2(source_path, destination_path)
    print("Successfully copied filtered movie file to destination.\n")
except Exception as e:
    print(f"Error while copying file: {e}")
    sys.exit(1)


repo_path = r"C:\Users\Satish Yadav\OneDrive\Desktop\Satish Coding\MovieStore\Backend"

try:
    os.chdir(repo_path)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "new movies added"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("Changes pushed to GitHub successfully.\n")
except subprocess.CalledProcessError as e:
    print(f"Git operation failed: {e}")
