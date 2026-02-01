from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from users.permissions import IsLibrarianOrAdmin

from .models import Author, Book, Genre, Location
from .serializers import (AuthorSerializer, BookCreateUpdateSerializer,
                          BookSerializer, GenreSerializer, LocationSerializer)


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления книгами.
    Поддерживает фильтрацию, поиск и сортировку.
    Создание, обновление и удаление доступны только библиотекарям и администраторам.
    """

    queryset = Book.objects.all().order_by("id")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["author", "genre", "publication_year"]
    search_fields = ["title", "description", "author__name", "genre__name"]
    ordering_fields = ["publication_year", "title"]
    ordering = ["id"]

    def get_permissions(self):
        """
        Ограничение прав для изменения данных: только для библиотекарей и админов.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsLibrarianOrAdmin()]
        return []

    def get_serializer_class(self):
        """
        Использует разные сериализаторы для чтения и записи.
        """
        if self.action in ["create", "update", "partial_update"]:
            return BookCreateUpdateSerializer
        return BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления авторами.
    Доступен только библиотекарям и администраторам.
    """

    queryset = Author.objects.all().order_by("id")
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarianOrAdmin]


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления жанрами книг.
    Доступен только библиотекарям и администраторам.
    """

    queryset = Genre.objects.all().order_by("id")
    serializer_class = GenreSerializer
    permission_classes = [IsLibrarianOrAdmin]


class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления местоположениями книг.
    Доступен только библиотекарям и администраторам.
    """

    queryset = Location.objects.all().order_by("id")
    serializer_class = LocationSerializer
    permission_classes = [IsLibrarianOrAdmin]
