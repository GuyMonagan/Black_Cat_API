from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "created_at", "is_approved")
    list_filter = ("is_approved", "rating", "created_at")
    search_fields = ("user__email", "book__title", "text")
    list_editable = ("is_approved",)
