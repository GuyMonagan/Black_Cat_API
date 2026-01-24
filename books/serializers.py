from rest_framework import serializers
from .models import Book, Author, Genre, Location


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'address', 'shelf_code']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()
    location = LocationSerializer()
    cover = serializers.ImageField(required=False)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'author', 'genre',
            'cover', 'total_count', 'available_count', 'location',
            'publisher', 'isbn', 'publication_year'
        ]


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'description', 'author', 'genre',
            'cover', 'total_count', 'available_count', 'location',
            'publisher', 'isbn', 'publication_year'
        ]
