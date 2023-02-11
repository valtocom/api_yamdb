import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import (
    Categories, Genres, GenreTitle, Title, Review, Comments, User
)


class Command(BaseCommand):
    """Переводит конкретные csv файлы
    (по  адресу 'static/data/') в базу данных проекта:
     python manage.py fill_database """

    help = 'Перевод из csv файлов в модели проекта'

    def fill_category(self):
        """Заполнение модели Categories"""
        with open(
            os.path.join('static/data/category.csv'),
            'r', encoding='utf-8'
        ) as csv_file:
            data = csv.DictReader(csv_file)
            for item in data:
                Categories.objects.get_or_create(
                    id=item['id'], name=item['name'], slug=item['slug']
                )

    def fill_genre(self):
        """Заполнение модели Genres"""
        with open(
            os.path.join('static/data/category.csv'),
            'r', encoding='utf-8'
        ) as csv_file:
            data = csv.DictReader(csv_file)
            for item in data:
                Genres.objects.get_or_create(
                    id=item['id'], name=item['name'], slug=item['slug']
                )

    def fill_title(self):
        """Заполнение модели Title"""
        with open(
            os.path.join('static/data/category.csv'),
            'r', encoding='utf-8'
        ) as csv_file:
            data = csv.DictReader(csv_file)
            for item in data:
                Title.objects.get_or_create(
                    id=item['id'], name=item['name'],
                    year=item['year'], category_id=item['category_id']
                )

    def fill_genre_title(self):
        """Заполнение модели GenreTitle"""
        with open(
            os.path.join('static/data/category.csv'),
            'r', encoding='utf-8'
        ) as csv_file:
            data = csv.DictReader(csv_file)
            for item in data:
                GenreTitle.objects.get_or_create(
                    id=item['id'], title_id=item['title_id'],
                    genre_id=item['genre_id']
                )

    def fill_review(self):
        """Заполнение модели Review"""
        with open(
            os.path.join('static/data/category.csv'),
            'r', encoding='utf-8'
        ) as csv_file:
            data = csv.DictReader(csv_file)
            for item in data:
                Review.objects.get_or_create(
                    id=item['id'], title_id=item['title_id'],
                    text=item['text'], author_id=item['author_id'],
                    score=item['score'], pub_date=item['pub_date']
                )

    def fill_comment(self):
        """Заполнение модели Comments"""
        with open(
            os.path.join('static/data/category.csv'),
            'r', encoding='utf-8'
        ) as csv_file:
            data = csv.DictReader(csv_file)
            for item in data:
                Comments.objects.get_or_create(
                    id=item['id'], review_id=item['review_id'],
                    text=item['text'], author_id=item['author_id'],
                    pub_date=item['pub_date']
                )

    def fill_user(self):
        """Заполнение модели User"""
        with open(
            os.path.join('static/data/category.csv'),
            'r', encoding='utf-8'
        ) as csv_file:
            data = csv.DictReader(csv_file)
            for item in data:
                User.objects.get_or_create(
                    id=item['id'], username=item['username'],
                    email=item['email'], role=item['role'],
                    bio=item['bio'], first_name=item['first_name'],
                    last_name=item['last_name']
                )

    def handle(self, *args, **options):
        self.fill_category()
        self.fill_genre()
        self.fill_title()
        self.fill_genre_title()
        self.fill_review()
        self.fill_comment()
        self.fill_user()
