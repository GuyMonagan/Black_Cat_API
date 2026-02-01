from django.contrib import admin
from .models import Borrowing

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    """
    Админка для модели аренды книг.
    Поддерживает фильтрацию по датам и статусу возврата, поиск по пользователю и книге.
    """
    list_display = ("user", "book", "borrow_date", "return_date", "is_returned")
    list_filter = ("is_returned", "borrow_date", "return_date")
    search_fields = ("user__email", "book__title")
