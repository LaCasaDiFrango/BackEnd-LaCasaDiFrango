from rest_framework.serializers import ModelSerializer

from core.models.pedido.pedido import Pedido
from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import ItemPedidoSerializer

class PedidoSerializer(ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'status', 'total', 'itens')
        itens = ItemPedidoSerializer(many=True, read_only=True)
