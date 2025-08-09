from rest_framework.permissions import BasePermission, SAFE_METHODS
from core.models.usuario.user import User

class IsPedidoOwnerOrAdmin(BasePermission):
    """
    Permite acesso se o recurso estiver relacionado a um Pedido do usuário,
    ou se o usuário for administrador (perfil ou grupo).
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        print(f'[DEBUG IsPedidoOwnerOrAdmin] Usuário: {user}, Autenticado: {user.is_authenticated if user else "None"}')
        
        if not user or not user.is_authenticated:
            print('[DEBUG IsPedidoOwnerOrAdmin] Usuário não autenticado.')
            return False
        
        is_admin = (
            user.is_superuser or
            user.groups.filter(name='administradores').exists() or
            getattr(user, 'perfil', None) == 'administrador'
        )
        print(f'[DEBUG IsPedidoOwnerOrAdmin] is_admin: {is_admin}')
        
        try:
            owns_pedido = obj.pedido.usuario == user
            print(f'[DEBUG IsPedidoOwnerOrAdmin] owns_pedido: {owns_pedido}')
            result = is_admin or owns_pedido
        except AttributeError:
            print('[DEBUG IsPedidoOwnerOrAdmin] AttributeError no objeto, retornando False')
            result = False

        print(f'[DEBUG IsPedidoOwnerOrAdmin] Permissão concedida: {result}')
        return result


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        print(f'[DEBUG IsOwnerOrAdmin] Usuário: {user}, Autenticado: {user.is_authenticated if user else "None"}')
        
        if not user or not user.is_authenticated:
            print('[DEBUG IsOwnerOrAdmin] Usuário não autenticado.')
            return False

        is_admin = (
            user.is_superuser or
            user.groups.filter(name='administradores').exists() or
            getattr(user, 'perfil', None) == 'administrador'
        )
        print(f'[DEBUG IsOwnerOrAdmin] is_admin: {is_admin}')
        
        # Se o obj for um User, compara diretamente
        if isinstance(obj, User):
            is_owner = obj == user
        else:
            is_owner = getattr(obj, 'usuario', None) == user

        print(f'[DEBUG IsOwnerOrAdmin] is_owner: {is_owner}')
        
        result = is_admin or is_owner
        print(f'[DEBUG IsOwnerOrAdmin] Permissão concedida: {result}')
        return result


class IsAdminUser(BasePermission):
    """
    Permite acesso apenas a administradores (perfil ou grupo ou superuser).
    """
    def has_permission(self, request, view):
        user = request.user
        print(f'[DEBUG IsAdminUser] Usuário: {user}, Autenticado: {user.is_authenticated if user else "None"}')
        
        result = bool(
            user and
            user.is_authenticated and
            (
                user.is_superuser or
                user.groups.filter(name='administradores').exists() or
                getattr(user, 'perfil', None) == 'administrador'
            )
        )
        print(f'[DEBUG IsAdminUser] Permissão concedida: {result}')
        return result


class IsConsumerUser(BasePermission):
    """
    Permite acesso apenas a consumidores (perfil ou grupo).
    """
    def has_permission(self, request, view):
        user = request.user
        print(f'[DEBUG IsConsumerUser] Usuário: {user}, Autenticado: {user.is_authenticated if user else "None"}')

        result = bool(
            user and
            user.is_authenticated and
            (
                user.groups.filter(name='usuarios').exists() or
                getattr(user, 'perfil', None) == 'usuario'
            )
        )
        print(f'[DEBUG IsConsumerUser] Permissão concedida: {result}')
        return result


class IsGuestOrReadOnly(BasePermission):
    """
    Permite acesso de leitura para qualquer pessoa (inclusive não autenticada).
    Só usuários autenticados podem modificar.
    """
    def has_permission(self, request, view):
        print(f'[DEBUG IsGuestOrReadOnly] Método: {request.method}')
        if request.method in SAFE_METHODS:
            print('[DEBUG IsGuestOrReadOnly] Método seguro (leitura), permissão concedida.')
            return True
        user = request.user
        result = bool(user and user.is_authenticated)
        print(f'[DEBUG IsGuestOrReadOnly] Usuário autenticado: {result}')
        return result
