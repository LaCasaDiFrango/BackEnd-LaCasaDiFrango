from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPedidoOwnerOrAdmin(BasePermission):
    """
    Permite acesso se o recurso estiver relacionado a um Pedido do usuário,
    ou se o usuário for administrador.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        is_admin = user.is_superuser or user.groups.filter(name='administradores').exists()

        try:
            return is_admin or obj.pedido.usuario == user
        except AttributeError:
            return False  # obj não tem campo pedido ou pedido não tem usuario


class IsOwnerOrAdmin(BasePermission):
    """
    Permite acesso se o objeto for do usuário autenticado
    ou se o usuário for administrador/superuser.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        is_admin = user.is_superuser or user.groups.filter(name='administradores').exists()

        # Para funcionar, o objeto precisa ter um campo 'usuario'
        return is_admin or getattr(obj, 'usuario', None) == user


class IsAdminUser(BasePermission):
    """
    Permite acesso apenas a administradores (grupo 'administradores' ou superuser).
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
