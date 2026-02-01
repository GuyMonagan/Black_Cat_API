from datetime import datetime

from rest_framework import serializers

from .models import Author, Book, Genre, Location


class AuthorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели автора.
    Используется для отображения ID и имени автора.
    """

    class Meta:
        model = Author
        fields = ["id", "name"]


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для жанров книги.
    Отображает ID и название жанра.
    """

    class Meta:
        model = Genre
        fields = ["id", "name"]


class LocationSerializer(serializers.ModelSerializer):
    """
    Сериализатор местоположения книги.
    Используется для отображения адреса и кода полки.
    """

    class Meta:
        model = Location
        fields = ["id", "address", "shelf_code"]


class BookSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения полной информации о книге.
    Используется для чтения данных, включает вложенные сериализаторы.
    """

    author = AuthorSerializer()
    genre = GenreSerializer()
    location = LocationSerializer()
    cover = serializers.ImageField(required=False)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "author",
            "genre",
            "cover",
            "total_count",
            "available_count",
            "location",
            "publisher",
            "isbn",
            "publication_year",
        ]


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления книги.
    Включает валидацию полей total_count, isbn, publication_year и title.
    """

    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "author",
            "genre",
            "cover",
            "total_count",
            "available_count",
            "location",
            "publisher",
            "isbn",
            "publication_year",
        ]

    def validate(self, data):
        """
        Проверка: доступных книг не может быть больше, чем всего.
        """
        total = data.get("total_count")
        available = data.get("available_count")

        if total is not None and available is not None and available > total:
            raise serializers.ValidationError(
                "Доступных экземпляров не может быть больше, чем всего."
            )

        return data

    def validate_isbn(self, value):
        """
        Валидация ISBN: только цифры и тире.
        """
        if value and not value.replace("-", "").isdigit():
            raise serializers.ValidationError(
                "ISBN должен содержать только цифры и тире."
            )
        return value

    def validate_publication_year(self, value):
        """
        Проверка: год публикации не может быть в будущем.
        """
        current_year = datetime.now().year
        if value and value > current_year:
            raise serializers.ValidationError("Год публикации не может быть в будущем.")
        return value

    def validate_title(self, value):
        """
        Проверка: название книги не должно быть пустым.
        """
        if not value.strip():
            raise serializers.ValidationError("Название книги не может быть пустым.")
        return value
