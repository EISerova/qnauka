import urllib.request
import json
import os

from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

BOT_DEBUG_TOKEN = os.getenv('BOT_DEBUG_TOKEN') 
CHAT_ID = os.getenv('CHAT_ID')


def send_telegram_message(chat_id, post):
    api_url = f'https://api.telegram.org/bot{BOT_DEBUG_TOKEN}/sendMessage'

    input_data = json.dumps(
        {
            'chat_id': chat_id,
            'text': post,
            'parse_mode': "HTML"
        }
    ).encode()

    try:
        req = urllib.request.Request(
            url=api_url,
            data=input_data,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            print(response.read().decode('utf-8'))

    except Exception as e:
        print(e)

# import urllib.request
# import json
# import os

# from django.conf import settings
# from dotenv import load_dotenv
# load_dotenv()

# from .telegram_utils import get_html_message_from_template

# BOT_TOKEN = os.getenv('BOT_TOKEN') 
# CHAT_ID = os.getenv('CHAT_ID')

# def send_telegram_message(chat_id, post):
#     api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

#     input_data = json.dumps(
#         {
#             'chat_id': chat_id,
#             'text': get_html_message_from_template(post=post),
#             'parse_mode': "HTML"
#         }
#     ).encode()

#     try:
#         req = urllib.request.Request(
#             url=api_url,
#             data=input_data,
#             headers={'Content-Type': 'application/json'}
#         )
#         with urllib.request.urlopen(req) as response:
#             print(response.read().decode('utf-8'))

#     except Exception as e:
#         print(e)