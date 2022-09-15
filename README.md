# Проект Yatube
[![Python](https://img.shields.io/badge/Made%20with-Python-green?logo=python&logoColor=white&color)](https://www.python.org/)
[![Django](https://img.shields.io/static/v1?message=django&logo=django&labelColor=5c5c5c&color=0c4b33&logoColor=white&label=%20&style=plastic)](https://www.djangoproject.com/)
[![Postgres](https://img.shields.io/static/v1?message=postgresql&logo=postgresql&labelColor=5c5c5c&color=1182c3&logoColor=white&label=%20&style=plastic)](https://www.postgresql.org/)


## О проекте:
**Социальная  сеть для публикации личных дневников.**

### Возможности проекта:
- можно создать свою страницу;
- пользователи могут заходить на чужие страницы, подписываться на авторов и комментировать их записи;
- автор может выбрать имя и уникальный адрес для своей страницы.

### Запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:
```sh
git clone git@github.com:s-antoshkin/hw05_final.git
```
Скопировать `.env.example` и назвать его `.env`:
```sh
cp .env.example .env
```
Заполнить переменные окружения в `.env`:
```sh
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД

SECRET_KEY=secret_key # секретный ключ (вставте свой)
```
Установить и активировать виртуальное окружение:
```sh
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt
```sh
pip install -r requirements.txt
```
Импортировать данные:
```sh
python manage.py loaddata dump.json
```
Собрать статику и выполнить миграции, создать суперпользователя:
```sh
python manage.py migrate --noinput
python manage.py createsuperuser
python manage.py collectstatic --no-input
```
Запустить проект:
```sh
python manage.py runserver
```
Проект будет доступен по [адресу](http://127.0.0.1:8000/).
