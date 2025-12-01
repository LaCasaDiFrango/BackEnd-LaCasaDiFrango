from rest_framework import serializers
from core.models.usuario.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Incluímos explicitamente os campos importantes + ultimo_pedido
        fields = [
            'id',
            'name',
            'email',
            'perfil',
            'passage_id',
            'endereco',
            'is_active',
            'is_staff',
            'ultimo_pedido',  # ⚡ Adicionado
        ]
        depth = 1


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Incluímos ultimo_pedido para listar usuários ativos/inativos
        fields = ("id", "name", "email", "perfil", "ultimo_pedido")
    