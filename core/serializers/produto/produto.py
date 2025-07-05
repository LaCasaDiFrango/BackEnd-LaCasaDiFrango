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

class ProdutoAjustarEstoqueSerializer(Serializer):
    quantidade_em_estoque = IntegerField()

    def validate_quantidade(self, value):
        produto = self.context.get('produto')
        if produto:
            nova_quantidade = produto.quantidade_em_estoque + value
            if nova_quantidade < 0:
                raise ValidationError('A quantidade em estoque não pode ser negativa.')
        return value
