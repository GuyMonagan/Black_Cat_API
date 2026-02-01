from rest_framework.permissions import BasePermission


class IsOwnerOrLibrarianOrAdmin(BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта,
    библиотекарем или администратором.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.user == request.user or request.user.role in ["librarian", "admin"]
