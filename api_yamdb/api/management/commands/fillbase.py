import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import (
    Categories, Genres, GenreTitle, Titles, Reviews, Comments, User)


class Command(BaseCommand):
    """Переводит конкретные csv файлы
    (по  адресу 'static/data/') в базу данных проекта:
     python manage.py fill_database """

    help = 'Перевод из csv файлов в модели проекта'

    def fill_category(self):
        """Заполнение модели Categories"""
        with open(os.path.join('static/data/category.csv'),
                  'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            for item in data:
                if item[0] != 'id':
                    Categories.objects.get_or_create(
                        id=item[0], name=item[1], slug=item[2])
  
    def fill_genre(self):
        """Заполнение модели Genres"""
        with open(os.path.join('static/data/genre.csv'),
                  'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            for item in data:
                if item[0] != 'id':
                    Genres.objects.get_or_create(
                        id=item[0], name=item[1], slug=item[2])

    def fill_title(self):
        """Заполнение модели Titles"""
        with open(os.path.join('static/data/titles.csv'),
                  'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            for item in data:
                if item[0] != 'id':
                    Titles.objects.get_or_create(
                        id=item[0], name=item[1],
                        year=item[2], category_id=item[3])

    def fill_genre_title(self):
        """Заполнение модели GenreTitle"""
        with open(os.path.join('static/data/genre_title.csv'),
                  'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            for item in data:
                if item[0] != 'id':
                    GenreTitle.objects.get_or_create(
                        id=item[0], title_id=item[1], genre_id=item[2])

    def fill_review(self):
        """Заполнение модели Reviews"""
        with open(os.path.join('static/data/review.csv'),
                  'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            for item in data:
                if item[0] != 'id':
                    Reviews.objects.get_or_create(
                        id=item[0], title_id=item[1],
                        text=item[2], author_id=item[3],
                        score=item[4], pub_date=item[5])

    def fill_comment(self):
        """Заполнение модели Comments"""
        with open(os.path.join('static/data/comments.csv'),
                  'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            for item in data:
                if item[0] != 'id':
                    Comments.objects.get_or_create(
                        id=item[0], review_id=item[1],
                        text=item[2], author_id=item[3],
                        pub_date=item[4])

    def fill_user(self):
        """Заполнение модели User"""
        with open(os.path.join('static/data/users.csv'),
                  'r', encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            for item in data:
                if item[0] != 'id':
                    User.objects.get_or_create(
                        id=item[0], username=item[1],
                        email=item[2], role=item[3],
                        bio=item[4], first_name=item[5],
                        last_name=item[6])

    def handle(self, *args, **options):
        self.fill_category()
        self.fill_genre()
        self.fill_title()
        self.fill_genre_title()
        self.fill_review()
        self.fill_comment()
        self.fill_user()
