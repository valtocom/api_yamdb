import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Titles, Categories, Genres, Reviews, Comments, User



class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()



class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для объектов Categories. Включает все поля. '''
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    '''Сериализатор для объектов Genres. Включает все поля. '''
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitleSerializerCreate(serializers.ModelSerializer):
    '''Сериализатор для объектов Title при создании.
    Проводит проверку на коррегдность года создания'''
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True)

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Titles

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год создания!')
        return value


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при чтении.
    Высчитывает отдельное поле - рейтинг произведения"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = ('name', 'year', 'description',
                  'genre', 'category', 'id', 'rating')
        read_only_fields = ('id',)

    def get_rating(self, obj):
        rating = Reviews.objects.all().aggregate(Avg('score'))
        return rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
        read_only_fields = ('pub_date',)
