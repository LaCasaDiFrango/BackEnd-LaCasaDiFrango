from rest_framework.serializers import ModelSerializer

from core.models.pedido.pedido import Pedido
from core.serializers.pedido.item_pedido import ItemPedidoSerializer

class PedidoSerializer(ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        itens = ItemPedidoSerializer(many=True, read_only=True)
