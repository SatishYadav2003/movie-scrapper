import subprocess
import os

script1 = "main.py"
script2 = os.path.join("helper", "movie4u_movie_update_automate.py")

try:
    print("Running main.py...\n")
    subprocess.run(f'python "{script1}"', shell=True, check=True)

    print("Running movie4u_movie_update_automate.py...\n")
    subprocess.run(f'python "{script2}"', shell=True, check=True)

    print("\nAll scripts executed successfully!")

except subprocess.CalledProcessError as e:
    print(f"\nError executing scripts: {e}")
