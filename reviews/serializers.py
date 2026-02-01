from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения отзыва.
    Содержит информацию о пользователе, книге, рейтинге и тексте.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'text', 'rating', 'created_at', 'is_approved']
        read_only_fields = ['is_approved', 'user', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и редактирования отзыва.
    Пользователь и статус модерации не указываются вручную.
    """
    class Meta:
        model = Review
        fields = ['book', 'text', 'rating']
