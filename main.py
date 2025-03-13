# # import time
# # import schedule
# from helper.helper_methods import execute_driver
# from movie_scrapper import movie_scrapping_begin


# driver = execute_driver()

# def execute_movie_scrapper_fun():
#     movie_scrapping_begin(driver)
    
 

# execute_movie_scrapper_fun()



# # schedule.every(5).seconds.do(execute_movie_scrapper_fun)


# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)



from fastapi import FastAPI
import asyncio
from helper.helper_methods import execute_driver
from movie_scrapper import movie_scrapping_begin

app = FastAPI()

driver = execute_driver()

async def execute_movie_scrapper_fun():
    await asyncio.to_thread(movie_scrapping_begin, driver)  # Run in a separate thread

@app.post("/start-scrape")
async def start_scrape():
    await execute_movie_scrapper_fun()
    return {"message": "Scraping started!"}

