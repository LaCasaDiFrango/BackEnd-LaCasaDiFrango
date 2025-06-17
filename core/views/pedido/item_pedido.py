from rest_framework.viewsets import ModelViewSet

from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import ItemPedidoSerializer

class ItemPedidoViewSet(ModelViewSet):
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer