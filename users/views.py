from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import TelegramToken

from .serializers import (UserRegisterSerializer, UserSerializer,
                          UserUpdateSerializer)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации новых пользователей.
    Доступен всем.
    """

    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    """
    Эндпоинт для получения информации о текущем пользователе.
    """

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MeUpdateView(generics.UpdateAPIView):
    """
    Эндпоинт для редактирования данных текущего пользователя.
    Требует авторизации.
    """

    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class GenerateTelegramTokenView(APIView):
    """
    Создаёт или возвращает одноразовый токен для привязки Telegram-аккаунта.
    Требует авторизации.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_obj, _ = TelegramToken.objects.get_or_create(user=request.user)
        return Response({"token": str(token_obj.token)})
