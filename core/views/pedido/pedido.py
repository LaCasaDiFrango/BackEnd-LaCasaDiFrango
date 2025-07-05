from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone

from core.models.pedido.pedido import Pedido
from core.serializers.pedido.pedido import PedidoSerializer, PedidoCreateUpdateSerializer, PedidoListSerializer


class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PedidoListSerializer
        if self.action in ('create', 'update'):
            return PedidoCreateUpdateSerializer
        return PedidoSerializer

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Pedido.objects.all()
        if usuario.groups.filter(name='administradores').exists():
            return Pedido.objects.all()
        return Pedido.objects.filter(usuario=usuario)

    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        pedido = self.get_object()

        if pedido.status != Pedido.StatusCompra.CARRINHO:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'status': 'pedido já finalizada'},
            )

        with transaction.atomic():
            for item in pedido.itens.all():

                if item.quantidade > item.produto.quantidade_em_estoque:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status': 'Quantidade insuficiente',
                            'produto': item.produto.nome,
                            'quantidade_disponivel': item.produto.quantidade_em_estoque,
                        },
                    )

                item.produto.quantidade_em_estoque -= item.quantidade
                item.produto.save()

            pedido.status = pedido.StatusCompra.FINALIZADO
            pedido.save()

        return Response(status=status.HTTP_200_OK, data={'status': 'Pedido finalizada'})

    @action(detail=False, methods=['get'])
    def relatorio_vendas_mes(self, request):
        agora = timezone.now()
        inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        pedidos = pedido.objects.filter(status=Pedido.StatusCompra.FINALIZADO, data__gte=inicio_mes)

        total_vendas = sum(pedido.total for pedido in pedidos)
        quantidade_vendas = pedidos.count()

        return Response(
            {
                'status': 'Relatório de vendas deste mês',
                'total_vendas': total_vendas,
                'quantidade_vendas': quantidade_vendas,
            },
            status=status.HTTP_200_OK,
        )