from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import TelegramToken

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MeUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class GenerateTelegramTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_obj, _ = TelegramToken.objects.get_or_create(user=request.user)
        return Response({"token": str(token_obj.token)})
