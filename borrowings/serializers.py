from rest_framework import serializers
from .models import Borrowing
from books.serializers import BookSerializer
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения информации об аренде книги.
    Включает данные о пользователе и книге.
    """
    user = UserSerializer(read_only=True)
    book = BookSerializer()

    class Meta:
        model = Borrowing
        fields = ['id', 'user', 'book', 'borrow_date', 'return_date', 'is_returned']


class BorrowingCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания новой аренды книги.
    Проверяет, что дата возврата не раньше даты заимствования.
    """
    expected_return_date = serializers.DateField(required=True)

    class Meta:
        model = Borrowing
        fields = ['book', 'borrow_date', 'expected_return_date']

    def validate(self, data):
        """
        Проверка: дата возврата не может быть раньше даты заимствования.
        """
        borrow = data.get("borrow_date")
        expected = data.get("expected_return_date")

        if borrow and expected and borrow > expected:
            raise serializers.ValidationError(
                "Ожидаемая дата возврата не может быть раньше даты заимствования."
            )
        return data
