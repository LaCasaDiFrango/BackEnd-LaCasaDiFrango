from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPedidoOwnerOrAdmin(BasePermission):
    """
    Permite acesso se o recurso estiver relacionado a um Pedido do usuário,
    ou se o usuário for administrador (perfil ou grupo).
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        
        is_admin = (
            user.is_superuser or
            user.groups.filter(name='administradores').exists() or
            getattr(user, 'perfil', None) == 'administrador'
        )
        try:
            return is_admin or obj.pedido.usuario == user
        except AttributeError:
            return False

class IsOwnerOrAdmin(BasePermission):
    """
    Permite acesso se o objeto for do usuário autenticado
    ou se o usuário for administrador (perfil ou grupo).
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        is_admin = (
            user.is_superuser or
            user.groups.filter(name='administradores').exists() or
            getattr(user, 'perfil', None) == 'administrador'
        )
        return is_admin or getattr(obj, 'usuario', None) == user

class IsAdminUser(BasePermission):
    """
    Permite acesso apenas a administradores (perfil ou grupo ou superuser).
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and
            user.is_authenticated and
            (
                user.is_superuser or
                user.groups.filter(name='administradores').exists() or
                getattr(user, 'perfil', None) == 'administrador'
            )
        )

class IsConsumerUser(BasePermission):
    """
    Permite acesso apenas a consumidores (perfil ou grupo).
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and
            user.is_authenticated and
            (
                user.groups.filter(name='usuarios').exists() or
                getattr(user, 'perfil', None) == 'usuario'
            )
        )

class IsGuestOrReadOnly(BasePermission):
    """
    Permite acesso de leitura para qualquer pessoa (inclusive não autenticada).
    Só usuários autenticados podem modificar.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated)
