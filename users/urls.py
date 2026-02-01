from django.urls import path

from .views import GenerateTelegramTokenView, MeUpdateView, MeView

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("me/update/", MeUpdateView.as_view(), name="me-update"),
    path("generate-telegram-token/", GenerateTelegramTokenView.as_view()),
]
