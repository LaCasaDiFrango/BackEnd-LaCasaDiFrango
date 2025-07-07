from rest_framework.viewsets import ModelViewSet

from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import (ItemPedidoSerializer, ItemPedidoCreateUpdateSerializer, ItemPedidoListSerializer,)
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser

class ItemPedidoViewSet(ModelViewSet):
    queryset = ItemPedido.objects.all()

    def get_permissions(self):
        # só acessa quem está autenticado, e para alterar só admin
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists():
            return ItemPedido.objects.all()
        # Para usuários comuns, só retorna itens dos pedidos deles
        return ItemPedido.objects.filter(pedido__usuario=user)
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ItemPedidoCreateUpdateSerializer
        if self.action == 'list':
            return ItemPedidoListSerializer
        return ItemPedidoSerializer