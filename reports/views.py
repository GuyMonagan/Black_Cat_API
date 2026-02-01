from datetime import timedelta

from django.db.models import Count
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from books.models import Book
from borrowings.models import Borrowing


class ReportsViewSet(viewsets.ViewSet):
    """
    ViewSet для получения различных отчётов по библиотеке.
    Доступ открыт всем пользователям (AllowAny).
    """

    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"])
    def popular_books(self, request):
        """
        Возвращает топ-10 самых часто арендуемых книг.
        """
        books = Book.objects.annotate(borrow_count=Count("borrowing")).order_by(
            "-borrow_count"
        )[:10]
        data = [
            {"title": book.title, "times_borrowed": book.borrow_count} for book in books
        ]
        return Response(data)

    @action(detail=False, methods=["get"])
    def debtors(self, request):
        """
        Возвращает список пользователей, которые не вернули книги вовремя.
        """
        today = now().date()
        borrowings = Borrowing.objects.filter(
            expected_return_date__lt=today, is_returned=False
        ).select_related("user", "book")

        data = [
            {
                "user": b.user.email,
                "book": b.book.title,
                "expected_return_date": b.expected_return_date,
            }
            for b in borrowings
        ]
        return Response(data)

    @action(detail=False, methods=["get"])
    def lost_books(self, request):
        """
        Возвращает список книг, которые не вернули более 30 дней.
        """
        threshold = now().date() - timedelta(days=30)
        lost = Borrowing.objects.filter(
            expected_return_date__lt=threshold, is_returned=False
        ).select_related("book", "user")

        data = [
            {
                "user": b.user.email,
                "book": b.book.title,
                "expected_return_date": b.expected_return_date,
            }
            for b in lost
        ]
        return Response(data)
