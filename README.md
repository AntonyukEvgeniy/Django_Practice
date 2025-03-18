# Django Practice Project
Учебный проект на Django для практики разработки веб-приложений.
## Технологии
- Python 3.13
- Django 5.1.7
- Bootstrap 5.3.3
- Poetry для управления зависимостями
## Зависимости для разработки
- flake8
- black 
- isort
## Установка и запуск
1. Клонируйте репозиторий:

```
bash
git clone <repository-url>
cd Django_Practice
```
2. Установите Poetry (если еще не установлен):
```
bash 
pip install poetry
```
3. Установите зависимости проекта:
```
bash
poetry install
```
4. Примените миграции:
```
bash 
poetry run python manage.py migrate
```
5. Запустите сервер разработки:
```
bash
poetry run python manage.py runserver
```
Приложение будет доступно по адресу: http://127.0.0.1:8000/
## Структура проекта
- `catalog/` - основное приложение
- `config/` - настройки проекта
- `static/` - статические файлы (CSS, JavaScript)
- `templates/` - HTML шаблоны
## Автор
Антонюк Евгений