from rest_framework.serializers import ModelSerializer

from core.models.produto.produto import Produto

class ProdutoSerializer(ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
