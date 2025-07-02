from rest_framework.serializers import ModelSerializer

from core.models.pedido.item_pedido import ItemPedido
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

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

class ItemPedidoListSerializer(ModelSerializer):
    produto = CharField(source='produto.nome', read_only=True)

    class Meta:
        model = ItemPedido
        fields = ('quantidade', 'produto')
        depth = 1