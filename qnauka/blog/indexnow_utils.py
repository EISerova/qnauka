"""Функция быстрого индексирования, отправляет ссылку на новость https://yandex.com/indexnow"""

import requests
import json

from qnauka.settings import INDEXNOW_KEY, CHAT_ID
# from .send_message import send_telegram_message

session = requests.Session()


def notify_indexnow(slug, category):
    url_searchengine = "https://yandex.com/indexnow"
    host = "https://qnauka.ru"
    params = {
        "url": f"{host}/{category}/{slug}",
        "key": INDEXNOW_KEY,
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = json.dumps(params)

    resp = session.get(url_searchengine, data=data, headers=headers)
    # send_telegram_message(CHAT_ID, f"{host}/{category}/{slug}")
