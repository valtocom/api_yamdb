from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    CHOICES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[validators.validate_slug]
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=True,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True,
    )

    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )

    role = models.CharField(
        verbose_name='Права пользователя',
        max_length=50,
        choices=CHOICES,
        default=USER,
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
