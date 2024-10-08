from django.template.loader import render_to_string

import os
import requests

from django.conf import settings

from qnauka.settings import HOST, BOT_TOKEN, CHAT_ID


def render_html_message(post):
    """Рендер шаблона сообщения для отправки в тг."""

    return render_to_string(
        "rss/telegram_post.html", {"post": post, "host": HOST}
        )


def send_message_to_telegram(post):
    """Отправка сообщения в тг после нажатия кнопки в админке."""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {"photo": post.image}
    data = {
        "chat_id": CHAT_ID,
        "caption": render_html_message(post=post),
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, files=files, data=data)
        # print(resp.text)
        return response
    except Exception as e:
        print(e)
