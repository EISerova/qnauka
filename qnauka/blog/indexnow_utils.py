import requests
import json

from qnauka.settings import INDEXNOW_KEY, HOST, CHAT_ID

# from .send_message import send_telegram_message

session = requests.Session()


def notify_indexnow(slug, category):
    """Функция быстрого индексирования, отправляет ссылку на новость https://yandex.com/indexnow"""

    url_searchengine = "https://yandex.com/indexnow"
    params = {
        "url": f"{HOST}/{category}/{slug}",
        "key": INDEXNOW_KEY,
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = json.dumps(params)

    session.get(url_searchengine, data=data, headers=headers)

    # resp = session.get(url_searchengine, data=data, headers=headers)
    # send_telegram_message(CHAT_ID, f'{host}/{category}/{slug}')
    # send_telegram_message(CHAT_ID, resp.status_code)
    # send_telegram_message(CHAT_ID, resp.text)
    # send_telegram_message(CHAT_ID, resp.data)
    # send_telegram_message(CHAT_ID, resp.headers)
    # send_telegram_message(CHAT_ID, resp.content_type)
