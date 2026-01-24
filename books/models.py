from django.db import models

class Author(models.Model):
    """
    Модель автора книги.

    Поля:
    - name: Полное имя автора.

    Методы:
    - __str__: Возвращает имя автора.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Genre(models.Model):
    """
    Модель жанра книги.

    Поля:
    - name: Название жанра (например, 'Фэнтези', 'Детектив').

    Методы:
    - __str__: Возвращает название жанра.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    """
    Модель хранения информации о местоположении книги.

    Поля:
    - address: Адрес библиотеки или помещения (может быть пустым).
    - shelf_code: Код ячейки или полки, где находится книга (например, 'A3-2').

    Методы:
    - __str__: Возвращает строку с адресом и кодом ячейки.
    """
    address = models.CharField(max_length=255, blank=True, null=True)
    shelf_code = models.CharField(max_length=50, help_text="Например: A3-2")

    def __str__(self):
        return f"{self.address or 'Без адреса'} — ячейка {self.shelf_code}"

class Book(models.Model):
    """
    Модель книги в библиотечной системе.

    Поля:
    - title: Название книги.
    - description: Описание или аннотация (опционально).
    - author: Автор книги (связь с моделью Author).
    - genre: Жанр книги (связь с Genre, может быть null).
    - cover: Обложка книги (опционально, сохраняется в 'book_covers/').
    - total_count: Общее количество экземпляров.
    - available_count: Количество доступных экземпляров.
    - location: Местоположение книги (связь с Location, может быть пустым).

    Методы:
    - __str__: Возвращает название книги.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    total_count = models.PositiveIntegerField(default=1)
    available_count = models.PositiveIntegerField(default=1)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    publisher = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True, unique=True)
    publication_year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title
