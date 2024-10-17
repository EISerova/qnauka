
# Qnauka - научный блог

Новостной сайт на Django. Статьи разбиты по категориям и тегам, при публикации анонс отправляется в telegram-канал.

## Скриншоты:
Главная страница
![Main page screenshot](https://i.ibb.co/W5jNmsR/main.jpg)

## Автор: 
Серова Екатерина

## Обратная связь:
Если у вас есть предложения или замечания, пожалуйста, свяжитесь со мной - katyaserova@yandex.ru

## Запуск проекта в dev-режиме

Клонировать репозиторий

```bash
  git clone https://github.com/EISerova/qnauka
```

Перейти в папку проекта

Создать и активировать виртуальное окружение

```bash
  python3 -m venv env
  source env/bin/activate
```

Установить зависимости

```bash
  python -m pip install --upgrade pip
  pip install -r requirements.txt
```

Выполнить миграции

```bash
  cd qnauka
  python manage.py migrate
```

Запустить сервер

```bash
  python manage.py runserver
```


## Переменные окружения

Чтобы запустить этот проект, вам нужно добавить в файл .env переменные, указанные в .env.example

## Demo

https://qnauka.ru/


## Лицензия:
[MIT](https://choosealicense.com/licenses/mit/)