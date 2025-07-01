from rest_framework.serializers import ModelSerializer

from core.models.usuario.user import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")
