from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from telegram_api import telegram_message_forward
from logging_info import log_message



from utils.date_provide import date_provide
import json
import time
import random



import os
from dotenv import load_dotenv



load_dotenv()


# import chromedriver_autoinstaller
# chromedriver_autoinstaller.install() 

service = Service(ChromeDriverManager().install())

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--disable-gpu")

# chrome_options = Options()
# chrome_options.add_argument("--headless")             # Run Chrome in headless mode (no GUI)
# chrome_options.add_argument("--window-size=1920x1080")    # Define a window size (even headless)
# chrome_options.add_argument("--no-sandbox")             # Disable the sandbox for security issues in Linux
# chrome_options.add_argument("--disable-dev-shm-usage")    # Overcome limited resource problems
# chrome_options.add_argument("--disable-gpu") 



# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(service=service)

# service = Service() 
# driver = webdriver.Chrome(service=service, options=chrome_options)


def execute_driver():
    return driver


def save_current_movie_name(movie_name):
    with open("previous_movie_name.txt","w",encoding="utf-8") as file:
        file.write(movie_name)
        
 
def get_previous_movie_name():  
    try:
        with open("previous_movie_name.txt","r",encoding="utf-8") as file:
           previous_movie_name =  file.read().strip()
           return previous_movie_name
    except FileNotFoundError as e:
        return f"No_data_exist: {e.filename}"
  
  
  
def get_current_movie_link(xpath_condition):
    text_href_detail = driver.execute_script("return arguments[0].getAttribute('href');",xpath_condition)
    return text_href_detail
 
  
def get_current_movie_name(movie,xpath_condition):                  
    text_detail = movie.find_element(By.XPATH,xpath_condition)
    return text_detail.text
  
 
def reset_url():
    time.sleep(random.uniform(4, 10)) 
    driver.get(os.getenv("MP4_MOVIEZ_LINK"))



def check_ready_state():
    WebDriverWait(driver,30).until(
            lambda driver: driver.execute_script("return document.readyState")=="complete"
        )


def save_compiled_movie_details(movie_details_history):
    with open("compiled_movie_details.json","w",encoding="utf-8") as file:
            json.dump(movie_details_history,file,ensure_ascii=False,indent=4)


def load_compiled_movie_details():
      try:
           with open("compiled_movie_details.json", "r", encoding="utf-8") as file:
                return json.load(file)
      except (FileNotFoundError, json.JSONDecodeError):
                 return []

  
def scrap_current_movie_complete_details(movie_links):
    
    movie_details_history= load_compiled_movie_details()
    
    movie_image_all_url = []
    
    for movie_link in movie_links:
        
        time.sleep(random.uniform(4, 10)) 
        
        movie_link_anchor_tag = driver.find_element(By.XPATH,f"//a[@href='{movie_link}']")
        movie_link_of_a_movie = movie_link_anchor_tag.get_attribute("href")
        
        movie_link_anchor_tag.click()
        
        check_ready_state()
        
        time.sleep(random.uniform(4, 10)) 
        
        movie_img_url = driver.find_element(By.XPATH, "//img[@class='posterss']").get_attribute("src")
        movie_detail_section = driver.find_elements(By.XPATH,"//div[contains(@class,'jatt')]")
        
        movie_detail_section = movie_detail_section[:8]
        
         
        movie_detail = {} 

        for div in movie_detail_section:  
            
                key = div.find_element(By.TAG_NAME, "b").text.strip().replace(" :", "") 
                value = div.find_element(By.XPATH, "./div").text.strip() 
                
                movie_detail[key] = value
        
       
                
        movie_detail["movie_link"] = movie_link_of_a_movie
        movie_detail["movie_img_url"] = movie_img_url 
        
        movie_image_all_url.append(movie_img_url)
        
        
        movie_download_quality_link_button = driver.find_element(By.XPATH,"//div[@style='text-align:left;']/a").get_attribute("href")
        movie_detail["download_page_link"] = movie_download_quality_link_button
        
        # chatgpt ka niche ka do line hain
        movie_id = movie_download_quality_link_button.split("/")[-1].split(".")[0] 
        movie_detail["movie_id"] = movie_id
         
            
        movie_details_history.insert(0,movie_detail)
       
        save_compiled_movie_details(movie_details_history)
        
        reset_url()
        

    return movie_image_all_url
   

def generate_movie_link_from_movie_lists(movie_lists):
    
    movie_links = []
    
    for movie in movie_lists:
        anchor_tag = movie.find_element(By.XPATH,"./a")
        anchor_link = get_current_movie_link(anchor_tag)
        movie_links.append(anchor_link)
        
    return movie_links   
    


def check_and_notify_user():
        
    log_message(f" Scrapping start: {date_provide()}")
    
    movie_lists,all_latest_movie_name_array,latest_movie_name = scrap_up_to_date_movie()
    

    
    if len(movie_lists) != 0 :
       movie_links = generate_movie_link_from_movie_lists(movie_lists)
       all_movie_img_url = scrap_current_movie_complete_details(movie_links)
       all_latest_movie_name_array.reverse() 
       telegram_message_forward(all_latest_movie_name_array,movie_links,all_movie_img_url)
       save_current_movie_name(latest_movie_name)
       
       log_message(f" Scrapped new movie: {date_provide()}")
       
    log_message(f" Scrapping end: {date_provide()}\n")
    # driver.close()
        
        
 
def scrap_up_to_date_movie():
    
    movie_lists = WebDriverWait(driver,30).until(
        lambda driver: driver.find_elements(By.XPATH,"//div[@class='fl']")
    )

    delete_index = 0
    is_movie_exist_in_latest_movie_section = False
  
    latest_movie_name = ""
    all_latest_movie_name_array = []
    
    
    
    for index,movie in enumerate(movie_lists):
        
        movie_text = get_current_movie_name(movie,".//span[@class='moviename']") 
        
        if latest_movie_name == "" : latest_movie_name=movie_text  
         
        if movie_text == get_previous_movie_name() :
            delete_index = index 
            is_movie_exist_in_latest_movie_section = True            
            break
        else:
            all_latest_movie_name_array.append(movie_text)
            
        
        
    
    
    if delete_index > 0 and is_movie_exist_in_latest_movie_section == True:
     movie_lists = movie_lists[:(delete_index)]
    elif is_movie_exist_in_latest_movie_section == True :
     movie_lists = []       
      
    movie_lists.reverse()
    
    return [movie_lists,all_latest_movie_name_array,latest_movie_name]


