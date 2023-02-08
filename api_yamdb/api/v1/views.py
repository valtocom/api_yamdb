from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Titles, Categories, Genres, Reviews, User
from .permissions import IsAdminOrReadOnly, IsAdmin
from .serializers import (TitleSerializerCreate, TitleSerializerRead, CategorySerializer,
                          GenreSerializer, ReviewSerializer, ReviewSerializer, UserSerializer, 
                          SignupSerializer, TokenSerializer, CommentSerializer)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class = UserSerializer
    )

    def users_own_profile(self, request):
        user = request.user
        
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SignupAPIView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        if User.objects.filter(
                username=username,
                email=email
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = get_object_or_404(User)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='YaMDb registration',
            message=f'Your confirmation code: {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User)
        
        if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateRetrieveDeleteViewSet(mixins.CreateModelMixin, 
                                  mixins.ListModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    pass 


class TitleViewSet(viewsets.ModelViewSet):
    '''Вьюсет для передачи и получения информации о
    модели Titles. Создает и удаляет админ.
    Нет методов retrieve и update.'''
    queryset = Titles.objects.all()
    serializer_class = TitleSerializerRead
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'description', 'genre')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(CreateRetrieveDeleteViewSet):
    '''Вьюсет для передачи и получения информации о
    модели Categories. Создает и удаляет админ.
    Нет методов retrieve и update.'''
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateRetrieveDeleteViewSet):
    '''Вьюсет для передачи и получения информации о
    модели Genres. Изменения вносит админ.'''
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ([
        permissions.IsAuthenticatedOrReadOnly,
    ])
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
    
    def get_review(self):
        return get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.select_related('title', 'author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
            review=self.get_review(),
        )
