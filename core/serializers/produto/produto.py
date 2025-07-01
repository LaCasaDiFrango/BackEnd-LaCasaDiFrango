from rest_framework.serializers import ModelSerializer

from core.models.produto.produto import Produto

class ProdutoSerializer(ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class ProdutoListSerializer(ModelSerializer):
    class Meta:
        model = Produto
        fields = ("id", "nome", "preco")

class ProdutoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"
        depth = 1
