from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


class Categories(models.Model):
    '''Модель для работы с категориями Titles
    (список категорий создают админы)'''
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.slug


class Genres(models.Model):
    '''Модель для работы с жанрами Titles
    (список категорий создают админы)'''
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.slug   


class Titles(models.Model):
    '''Модель для работы с произведениями
    (вносить новые могут админы)'''
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genres, through='GenreTitle')
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles', null=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    '''Модель для объединения жанров с произведениями
    (создается автоматически)'''    
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Reviews(models.Model):
    '''Модель для работы с отзывами
    (Писать могут пользователи, модераторы и админы)'''
    title = models.ForeignKey(
        Titles,
        null=True,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(blank=True, null = True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.text

    
class Comments(models.Model):
    '''Модель для работы с отзывами
    (Писать могут пользователи, модераторы и админы)'''
    title = models.ForeignKey(
        Titles,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.text