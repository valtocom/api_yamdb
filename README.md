# api_yamdb

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

## Описание

Яндекс Практикум. Спринт 10. Командный проект

## Как запустить проект

1. Клонировать репозиторий и перейти в него в командной строке:

   ```
   git clone https://github.com/valtocom/api_yamdb.git
   ```

   ```
   cd api_yamdb/
   ```

2. Cоздать и активировать виртуальное окружение:

   ```
   python -m venv venv
   ```

   ```
   # для OS Lunix и MacOS
   source venv/bin/activate

   # для OS Windows
   source venv/Scripts/activate
   ```

   ```
   python3 -m pip install --upgrade pip
   ```

3. Установить зависимости из файла requirements.txt:

   ```
   pip install -r requirements.txt
   ```

4. Выполнить миграции:

   ```
   python3 manage.py migrate
   ```

5. Запустить проект:

   ```
   python3 manage.py runserver
   ```

## Ресурсы

- Документация проекта
http://127.0.0.1:8000/redoc/


- Postman
https://www.postman.com/


## Авторы проекта
- Владимир Дмитриев
- Анатолий Соловов
- Антон Гуляев
