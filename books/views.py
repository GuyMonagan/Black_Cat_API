from rest_framework import viewsets, filters
from .models import Book, Author, Genre, Location
from .serializers import (
    BookSerializer,
    BookCreateUpdateSerializer,
    AuthorSerializer,
    GenreSerializer,
    LocationSerializer
)
from users.permissions import IsAdmin, IsLibrarianOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from users.permissions import IsLibrarianOrAdmin


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'genre', 'publication_year']
    search_fields = ['title', 'description', 'author__name', 'genre__name']
    ordering_fields = ['publication_year', 'title']
    ordering = ['id']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarianOrAdmin()]
        return []

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookCreateUpdateSerializer
        return BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarianOrAdmin]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = [IsLibrarianOrAdmin]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('id')
    serializer_class = LocationSerializer
    permission_classes = [IsLibrarianOrAdmin]
