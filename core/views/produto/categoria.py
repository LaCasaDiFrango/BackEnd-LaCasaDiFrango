from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser, IsGuestOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models.pedido.item_pedido import ItemPedido
from django.db.models import Sum

from core.models.produto.categoria import Categoria
from core.models.produto.produto import Produto
from core.serializers.produto.categoria import CategoriaSerializer

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        if self.action in ['list', 'retrieve', 'vendas']:
            return [IsGuestOrReadOnly()]
        return super().get_permissions()

    # NOVO: endpoint para vendas por categoria
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
