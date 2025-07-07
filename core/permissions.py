from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUser(BasePermission):
    """
    Permite acesso apenas a administradores (grupo 'Administrador' ou superuser).
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or user.groups.filter(name='administradores').exists()))


class IsConsumerUser(BasePermission):
    """
    Permite acesso apenas a consumidores (grupo 'Usuario').
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.groups.filter(name='usuarios').exists())


class IsGuestOrReadOnly(BasePermission):
    """
    Permite acesso de leitura para qualquer pessoa (inclusive não autenticada).
    Somente usuários autenticados podem modificar.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
