from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Review
from .permissions import IsOwnerOrLibrarianOrAdmin
from .serializers import ReviewCreateSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления отзывами.
    Поддерживает создание, просмотр, редактирование и одобрение отзывов.
    """

    queryset = Review.objects.all()

    def get_permissions(self):
        """
        Ограничение доступа к операциям:
        - Только владелец, библиотекарь или админ могут редактировать/удалять/одобрять.
        - Остальные действия доступны аутентифицированным пользователям.
        """
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrLibrarianOrAdmin()]
        elif self.action == "approve":
            return [IsOwnerOrLibrarianOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Фильтрует отзывы в зависимости от роли пользователя.
        - Обычные пользователи видят только одобренные отзывы.
        - Админы и библиотекари — все.
        """
        user = self.request.user

        if self.action == "approve" and user.is_authenticated:
            return Review.objects.all()

        if user.role in ["admin", "librarian"]:
            return Review.objects.all()

        return Review.objects.filter(is_approved=True)

    def get_serializer_class(self):
        """
        Использует разные сериализаторы для чтения и записи.
        """
        if self.action in ["create", "update", "partial_update"]:
            return ReviewCreateSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        """
        Присваивает текущего пользователя как автора отзыва.
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """
        Позволяет администратору или библиотекарю одобрить отзыв.
        """
        review = self.get_object()
        if request.user.role not in ["admin", "librarian"]:
            return Response({"detail": "Недостаточно прав"}, status=403)
        review.is_approved = True
        review.save()
        return Response({"detail": "Отзыв одобрен"})
