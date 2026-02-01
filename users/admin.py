from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TelegramToken

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Админка для модели пользователя.
    Включает поля Telegram, роли и аватар.
    """
    model = User
    list_display = ("email", "role", "is_staff", "telegram_chat_id")
    list_filter = ("role", "is_staff", "is_superuser")
    search_fields = ("email", "telegram_chat_id")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password", "avatar")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Telegram", {"fields": ("telegram_chat_id",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role"),
        }),
    )

@admin.register(TelegramToken)
class TelegramTokenAdmin(admin.ModelAdmin):
    """
    Админка для одноразовых Telegram-токенов.
    """
    list_display = ("user", "token", "created_at")
    readonly_fields = ("token", "created_at")
