import os
from dotenv import load_dotenv
from helper.helper_methods import check_and_notify_user


load_dotenv()


def movie_scrapping_begin(driver):
  try:
    driver.get(os.getenv("MP4_MOVIEZ_LINK"))  
    check_and_notify_user()
  except Exception as e:
    print("Something went wrong we will scrap again after 1 minutes: ",e)    




