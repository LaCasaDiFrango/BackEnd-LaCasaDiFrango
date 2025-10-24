from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsPedidoOwnerOrAdmin
from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import (
    ItemPedidoSerializer,
    ItemPedidoCreateUpdateSerializer,
    ItemPedidoListSerializer,
)
from app.pagination import CustomPagination


class ItemPedidoViewSet(ModelViewSet):
    queryset = ItemPedido.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['pedido', 'produto']
    search_fields = ['produto__nome']
    ordering_fields = ['preco', 'quantidade']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ItemPedidoCreateUpdateSerializer
        if self.action == 'list':
            return ItemPedidoListSerializer
        return ItemPedidoSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsPedidoOwnerOrAdmin()]
        return [IsAuthenticated()]
