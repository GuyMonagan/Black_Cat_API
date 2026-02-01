from django.urls import path
from .views import easter_egg

urlpatterns = [
    path("thanks/", easter_egg, name="easter-egg"),
]
