from django.template.loader import render_to_string

import urllib.request
import json
import os
import requests

from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN') 
CHAT_ID = os.getenv('CHAT_ID')


def get_html_message_from_template(post):
    return render_to_string('post_telegram_message.html', {
        'post': post
    })
    
def send(chat_id, post):
    data = {"chat_id": chat_id}
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?chat_id={chat_id}"
    


    files = {'photo': post.image}
    resp = requests.post(url, files=files)
    print(resp)
    return resp
    
    # api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    # input_data = json.dumps(
    #     {
    #         'chat_id': chat_id,
    #         'text': get_html_message_from_template(post=post),
    #         'parse_mode': "HTML"
    #     }
    # ).encode()

    # try:
    #     req = urllib.request.Request(
    #         url=api_url,
    #         data=input_data,
    #         headers={'Content-Type': 'application/json'}
    #     )
    #     print(post.image)
    #     with urllib.request.urlopen(req) as response:
    #         print(response.read().decode('utf-8'))

    # except Exception as e:
    #     print(e)
        



# def send_photo(chat_id, image_path, image_caption=""):
#     data = {"chat_id": chat_id, "caption": image_caption}
#     url = f"https://api.telegram.org/bot{_TOKEN}/sendPhoto?chat_id={chat_id}"
#     with open(image_path, "rb") as image_file:
#         ret = requests.post(url, data=data, files={"photo": image_file})
#     return ret.json()