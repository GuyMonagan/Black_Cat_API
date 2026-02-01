from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils.timezone import now
from django.db.models import Count
from borrowings.models import Borrowing
from books.models import Book

from datetime import timedelta
from rest_framework.permissions import AllowAny


class ReportsViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def popular_books(self, request):
        books = (
            Book.objects.annotate(borrow_count=Count("borrowing"))
            .order_by("-borrow_count")[:10]
        )
        data = [
            {"title": book.title, "times_borrowed": book.borrow_count}
            for book in books
        ]
        return Response(data)

    @action(detail=False, methods=['get'])
    def debtors(self, request):
        today = now().date()
        borrowings = Borrowing.objects.filter(
            expected_return_date__lt=today,
            is_returned=False
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

    @action(detail=False, methods=['get'])
    def lost_books(self, request):
        threshold = now().date() - timedelta(days=30)
        lost = Borrowing.objects.filter(
            expected_return_date__lt=threshold,
            is_returned=False
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
