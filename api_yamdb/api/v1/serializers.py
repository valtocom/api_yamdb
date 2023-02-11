import datetime as dt

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from users.models import User
from reviews.models import Title, Categories, Genres, Review, Comments


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для объектов Categories. Включает все поля."""
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов Genres. Включает все поля."""
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitleSerializerCreate(serializers.ModelSerializer):
    """Сериализатор для объектов Title при создании.
    Проводит проверку на коррегдность года создания."""
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год создания!')
        return value


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при чтении.
    Высчитывает отдельное поле - рейтинг произведения."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category', 'rating'
        )
        read_only_fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'title', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title', 'author',)

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'You have already written a review on this title!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'title', 'review', 'author', 'pub_date')
        model = Comments
        read_only_fields = ('title', 'author', 'review')
