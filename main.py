# import time
# import schedule
from helper.helper_methods import execute_driver
from movie_scrapper import movie_scrapping_begin


driver = execute_driver()

def execute_movie_scrapper_fun():
    movie_scrapping_begin(driver)
    driver.quit()

    
 

execute_movie_scrapper_fun()



# schedule.every(5).seconds.do(execute_movie_scrapper_fun)


# while True:
#     schedule.run_pending()
#     time.sleep(1)

