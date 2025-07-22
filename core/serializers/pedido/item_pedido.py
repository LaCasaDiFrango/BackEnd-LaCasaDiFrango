from core.models.produto.produto import Produto
from core.models.pedido.item_pedido import ItemPedido
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

# Novo serializer para exibir detalhes do produto no pedido
class ProdutoPedidoSerializer(ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'nome', 'preco', 'quantidade_em_estoque')

# Atualizado: agora inclui detalhes do produto no retorno
class ItemPedidoSerializer(ModelSerializer):
    produto = ProdutoPedidoSerializer(read_only=True)
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.produto.preco * instance.quantidade

    class Meta:
        model = ItemPedido
        fields = ('produto', 'quantidade', 'total')

# Usado na criação e atualização de pedidos
class ItemPedidoCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ('produto', 'quantidade')

    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError("Quantidade do item deve ser maior que zero.")
        return quantidade

    def validate(self, data):
        produto = data.get('produto')
        quantidade = data.get('quantidade')

        if produto is None or quantidade is None:
            raise ValidationError("Produto e quantidade são obrigatórios.")

        if quantidade > produto.quantidade_em_estoque:
            raise ValidationError("Quantidade do item maior que o estoque disponível.")

        return data

# Lista de itens em um pedido resumido (ex: listagem de pedidos)
class ItemPedidoListSerializer(ModelSerializer):
    produto = ProdutoPedidoSerializer(read_only=True)

    class Meta:
        model = ItemPedido
        fields = ('quantidade', 'produto')
        depth = 1
