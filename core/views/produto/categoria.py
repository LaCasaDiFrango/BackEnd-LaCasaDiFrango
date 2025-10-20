from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser, IsGuestOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models.pedido.item_pedido import ItemPedido
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from core.models.produto.categoria import Categoria
from core.serializers.produto.categoria import CategoriaSerializer
from app.pagination import CustomPagination


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    pagination_class = CustomPagination 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['descricao']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']
    ordering = ['nome']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        if self.action in ['list', 'retrieve', 'vendas']:
            return [IsGuestOrReadOnly()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='vendas')
    def vendas(self, request):
        categorias = Categoria.objects.all()
        labels = []
        data = []

        for categoria in categorias:
            total_vendas = ItemPedido.objects.filter(produto__categoria=categoria).aggregate(
                total=Sum('quantidade')
            )['total'] or 0
            labels.append(categoria.nome)
            data.append(total_vendas)

        chart_data = {
            "labels": labels,
            "datasets": [
                {
                    "label": "Vendas por Categoria",
                    "data": data,
                    "backgroundColor": [
                        "#1b3d1f",
                        "#3b82f6",
                        "#B91C1C",
                        "#facc15",
                        "#10b981",
                        "#f97316",
                    ],
                    "borderRadius": 10,
                }
            ],
        }
        return Response(chart_data)
