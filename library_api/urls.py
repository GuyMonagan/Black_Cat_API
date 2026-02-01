from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from books.views import (AuthorViewSet, BookViewSet, GenreViewSet,
                         LocationViewSet)
from borrowings.views import BorrowingViewSet
from reports.views import ReportsViewSet
from reviews.views import ReviewViewSet
from users.views import (GenerateTelegramTokenView, MeUpdateView, MeView,
                         RegisterView)

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version="v1",
        description="Документация API библиотечной системы",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"authors", AuthorViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"locations", LocationViewSet)
router.register(r"borrowings", BorrowingViewSet)
router.register(r"reviews", ReviewViewSet)
router.register("reports", ReportsViewSet, basename="reports")


urlpatterns = [
    path("admin/", admin.site.urls),
    # User-related endpoints
    path("api/users/register/", RegisterView.as_view(), name="user-register"),
    path("api/users/me/", MeView.as_view(), name="user-me"),
    path("api/users/me/update/", MeUpdateView.as_view(), name="user-me-update"),
    path(
        "api/users/telegram-token/",
        GenerateTelegramTokenView.as_view(),
        name="user-telegram-token",
    ),
    # JWT auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # API routers (books, reviews, borrowings, etc.)
    path("api/", include(router.urls)),
    # docs
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
]

if settings.DEBUG:  # dev only
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
