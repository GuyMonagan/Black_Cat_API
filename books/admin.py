from django.contrib import admin
from .models import Author, Genre, Location, Book
from reviews.models import Review
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse


class ReviewInline(admin.TabularInline):
    """
    Инлайн-редактирование отзывов в админке книги.
    Отображает отзывы как табличную часть в карточке книги.
    """
    model = Review
    extra = 0
    fields = ("user", "rating", "text", "is_approved", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Админка для модели Author.
    Позволяет искать авторов по имени.
    """
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Админка для модели Genre.
    Поиск и отображение жанров.
    """
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Админка для местоположений книг.
    Поддерживает поиск по адресу и коду полки.
    """
    list_display = ("address", "shelf_code")
    search_fields = ("address", "shelf_code")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Админка для модели Book.
    Поддерживает фильтрацию, поиск и просмотр отзывов.
    """

    list_display = ("title", "author", "genre", "available_count", "total_count", "report_links")
    list_filter = ("genre", "author", "location")

    search_fields = ("title", "author__name", "genre__name")
    inlines = [ReviewInline]

    def report_links(self, obj):
        return format_html(
            '<a href="{}" target="_blank">📊 Популярные книги</a>',
            reverse("reports-popular-books")  # Это важно!
        )
    report_links.short_description = "📈 Отчёты"
