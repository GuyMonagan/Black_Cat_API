from rest_framework import viewsets
from .models import Borrowing
from .serializers import BorrowingSerializer, BorrowingCreateSerializer
from users.permissions import IsReader, IsLibrarianOrAdmin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book', 'is_returned']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'reader':
            return Borrowing.objects.filter(user=user).order_by('-borrow_date')
        return Borrowing.objects.all().order_by('-borrow_date')

    def get_permissions(self):
        if self.action in ['create']:
            return [IsReader()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsLibrarianOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]

        if book.available_count < 1:
            raise serializers.ValidationError("Нет доступных экземпляров книги.")

        borrowing = serializer.save(user=self.request.user)

        # Уменьшаем количество доступных книг
        book.available_count -= 1
        book.save()

        # Отправка сообщения в Telegram (если есть ID)
        from core.telegram_bot import send_telegram_message

        user = self.request.user
        if user.telegram_chat_id:
            return_date = borrowing.expected_return_date
            date_str = return_date.strftime('%d.%m.%Y') if return_date else "не указана"
            message = (
                f"📚 Вы взяли книгу «{book.title}».\n"
                f"Дата возврата: {date_str}."
            )
            send_telegram_message(user.telegram_chat_id, message)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BorrowingCreateSerializer
        return BorrowingSerializer
