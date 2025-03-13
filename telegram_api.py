import os
import requests
import time
from urllib.parse import urljoin, quote_plus
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()



def resize_and_pad_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

  
    target_width = 500 
    target_height = 500 
    target_size = (target_width, target_height)
    img.thumbnail(target_size, Image.Resampling.LANCZOS)

   
    new_img = Image.new("RGB", target_size, (255, 255, 255))
    paste_position = (
        (target_size[0] - img.size[0]) // 2,
        (target_size[1] - img.size[1]) // 2,
    )
    new_img.paste(img, paste_position)

    img_bytes = BytesIO()
    new_img.save(img_bytes, format="JPEG", optimize=True,quality=100)
    img_bytes.seek(0)
    return img_bytes


def telegram_message_forward(all_latest_movie_name_array, movie_links, all_movie_img_url):
    
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    for movie_name, movie_link, movie_image_url in zip(all_latest_movie_name_array, movie_links, all_movie_img_url):
      
      
        movie_full_url = urljoin(os.getenv("MP4_MOVIEZ_LINK"), movie_link)
        
        
        shrink_url = os.getenv("SHRINK_TOKEN") + quote_plus(movie_full_url)
        customize_url_link = requests.get(shrink_url)
        customize_url_link_text = customize_url_link.json().get("shortenedUrl")
        
      
        message_body = f"""
        ********** Hello <b>Movie Lover</b> *********** 
        \nMovie-Alert : <b>We found new movie for you!</b>
        \nMovie-Name : <b>{movie_name}</b>
        \n<b>Movie-Link</b> : <a href="{customize_url_link_text}">Click Here to download</a>
        """
        
        resized_image = resize_and_pad_image(movie_image_url)
        
       
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": message_body,
            "parse_mode": "HTML"
        }
        
        files = {"photo": ("image.jpg", resized_image, "image/jpeg")}
        
  
        requests.post(url, data=payload, files=files)
        
    
        time.sleep(1)


