from .views import MeUpdateView
from .views import MeView
from django.urls import path
from .views import GenerateTelegramTokenView

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("me/update/", MeUpdateView.as_view(), name="me-update"),
    path("generate-telegram-token/", GenerateTelegramTokenView.as_view()),
]
