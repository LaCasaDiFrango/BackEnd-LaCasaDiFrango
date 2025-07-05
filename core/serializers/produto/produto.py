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

class ProdutoAlterarPrecoSerializer(Serializer):
    preco = DecimalField(max_digits=10, decimal_places=2)

    def validate_preco(self, value):
        '''Valida se o preço é um valor positivo.'''
        if value <= 0:
            raise ValidationError('O preço deve ser um valor positivo.')
        return value
