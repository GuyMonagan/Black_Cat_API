import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_user_can_register(api_client):
    """
    Проверяет, что пользователь может зарегистрироваться через API.
    """
    data = {
        "email": "newuser@lib.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = api_client.post("/api/users/register/", data)
    assert response.status_code == 201
    assert response.data["email"] == "newuser@lib.com"


@pytest.mark.django_db
def test_user_can_retrieve_own_profile(api_client):
    """
    Проверяет, что пользователь может получить свои данные (/me).
    """
    user = User.objects.create_user(email="me@lib.com", password="pass")
    api_client.force_authenticate(user=user)

    response = api_client.get("/api/users/me/")
    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_user_can_update_own_profile(api_client):
    """
    Проверяет, что пользователь может обновить своё имя через эндпоинт /me/update/.
    """
    user = User.objects.create_user(email="update@lib.com", password="pass")
    api_client.force_authenticate(user=user)

    response = api_client.patch("/api/users/me/update/", {"first_name": "Updated"})
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.first_name == "Updated"


@pytest.mark.django_db
def test_user_gets_telegram_token(api_client):
    """
    Проверяет, что авторизованный пользователь может получить Telegram-токен.
    """
    user = User.objects.create_user(email="tg@lib.com", password="pass")
    api_client.force_authenticate(user=user)

    response = api_client.post("/api/users/telegram-token/")
    assert response.status_code == 200
    assert "token" in response.data
