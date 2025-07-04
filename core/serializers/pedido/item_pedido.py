
from core.models.pedido.item_pedido import ItemPedido
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField, ValidationError

class ItemPedidoSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.produto.preco * instance.quantidade

    class Meta:
        model = ItemPedido
        fields = ('produto', 'quantidade', 'total')
        depth = 1

class ItemPedidoCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ('produto', 'quantidade')

    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior do que zero.')
        return quantidade

    def validate(self, item):
        if item['quantidade'] > item['produto'].quantidade:
            raise ValidationError('Quantidade de itens maior do que a quantidade em estoque.')
        return item

class ItemPedidoListSerializer(ModelSerializer):
    produto = CharField(source='produto.nome', read_only=True)

    class Meta:
        model = ItemPedido
        fields = ('quantidade', 'produto')
        depth = 1