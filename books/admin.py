from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from reviews.models import Review

from .models import Author, Book, Genre, Location


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
    Поддерживает фильтрацию, поиск, просмотр отзывов и отображение обложек.
    """

    list_display = (
        "title",
        "author",
        "genre",
        "available_count",
        "total_count",
        "report_links",
        "cover_preview",  # ⬅ Добавлено отображение обложки
    )

    list_filter = ("genre", "author", "location")
    search_fields = ("title", "author__name", "genre__name")
    inlines = [ReviewInline]
    readonly_fields = ("cover_preview",)  # ⬅ Чтобы обложка показывалась в карточке

    def report_links(self, obj):
        return format_html(
            '<a href="{}" target="_blank">📊 Популярные книги</a>',
            reverse("reports-popular-books"),
        )

    report_links.short_description = "📈 Отчёты"

    def cover_preview(self, obj):
        """
        Показывает миниатюру обложки книги в админке.
        """
        if obj.cover:
            return format_html(
                '<img src="{}" style="max-height: 200px;" />', obj.cover.url
            )
        return "—"

    cover_preview.short_description = "Обложка"
