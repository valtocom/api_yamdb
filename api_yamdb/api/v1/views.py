from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Titles, Categories, Genres, Reviews, Comments, User
#from .permissions import 
from .serializers import (TitleSerializerCreate, TitleSerializerRead, CategorySerializer,
                          GenreSerializer, ReviewSerializer, CommentSerializer)

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
    #permission_classes = (AdminOrReadOnly,)

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
    #permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateRetrieveDeleteViewSet):
    '''Вьюсет для передачи и получения информации о
    модели Genres. Изменения вносит админ.'''
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet():
    pass


class CommentViewSet():
    pass
