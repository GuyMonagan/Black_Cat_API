import pytest
from books.models import Author, Genre, Location, Book

@pytest.mark.django_db
def test_author_str():
    author = Author.objects.create(name="Тест Автор")
    assert str(author) == "Тест Автор"

@pytest.mark.django_db
def test_genre_str():
    genre = Genre.objects.create(name="Хоррор")
    assert str(genre) == "Хоррор"

@pytest.mark.django_db
def test_location_str():
    loc = Location.objects.create(address="Читальный зал", shelf_code="B-12")
    assert str(loc) == "Читальный зал — ячейка B-12"

@pytest.mark.django_db
def test_book_str_and_fields():
    author = Author.objects.create(name="Автор")
    genre = Genre.objects.create(name="Драма")
    location = Location.objects.create(address="Архив", shelf_code="X-1")

    book = Book.objects.create(
        title="Заголовок",
        description="Описание",
        author=author,
        genre=genre,
        total_count=3,
        available_count=2,
        location=location,
        publisher="Издательство",
        isbn="123-456-789",
        publication_year=2001,
    )

    assert str(book) == "Заголовок"
    assert book.genre.name == "Драма"
    assert book.author.name == "Автор"
    assert book.location.shelf_code == "X-1"
    assert book.total_count == 3
    assert book.available_count == 2
