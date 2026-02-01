from rest_framework import serializers
from .models import Book, Author, Genre, Location
from datetime import datetime


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

    def validate(self, data):
        total = data.get("total_count")
        available = data.get("available_count")

        if total is not None and available is not None and available > total:
            raise serializers.ValidationError(
                "Доступных экземпляров не может быть больше, чем всего."
            )

        return data

    def validate_isbn(self, value):
        if value and not value.replace("-", "").isdigit():
            raise serializers.ValidationError("ISBN должен содержать только цифры и тире.")
        return value

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value and value > current_year:
            raise serializers.ValidationError("Год публикации не может быть в будущем.")
        return value

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название книги не может быть пустым.")
        return value
