from rest_framework.viewsets import ModelViewSet

from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import (ItemPedidoSerializer, ItemPedidoCreateUpdateSerializer, ItemPedidoListSerializer,)

class ItemPedidoViewSet(ModelViewSet):
    queryset = ItemPedido.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ItemPedidoCreateUpdateSerializer
        if self.action == 'list':
            return ItemPedidoListSerializer
        return ItemPedidoSerializer
