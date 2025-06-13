from rest_framework.serializers import ModelSerializer

from core.models.usuario.cartao import Cartao

class CartaoSerializer(ModelSerializer):
    class Meta:
        model = Cartao
        fields = '__all__'
