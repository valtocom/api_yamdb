from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Titles, Categories, Genres, Reviews, Comments, User
from .permissions import 
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer, ReviewSerializer, CommentSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet():
    pass


class CommentViewSet():
    pass
