from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Доступ только для пользователей с ролью 'admin'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsLibrarian(BasePermission):
    """
    Доступ только для пользователей с ролью 'librarian'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'librarian'


class IsReader(BasePermission):
    """
    Доступ только для пользователей с ролью 'reader'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'reader'


class IsLibrarianOrAdmin(BasePermission):
    """
    Доступ для библиотекарей и администраторов.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['librarian', 'admin']
