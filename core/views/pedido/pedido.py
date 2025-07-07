from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone

from core.models.pedido.pedido import Pedido
from core.serializers.pedido.pedido import PedidoSerializer, PedidoCreateUpdateSerializer, PedidoListSerializer

from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser, IsOwnerOrAdmin

class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PedidoListSerializer
        if self.action in ('create', 'update'):
            return PedidoCreateUpdateSerializer
        return PedidoSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        if self.action == 'relatorio_vendas_mes':
            return [IsAuthenticated(), IsAdminUser()]
        if self.action == 'finalizar':
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]


    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser or usuario.groups.filter(name='administradores').exists():
            return Pedido.objects.all()
        return Pedido.objects.filter(usuario=usuario)

    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        pedido = self.get_object()

        #Garante que só o dono do pedido ou admin finalize
        if pedido.usuario != request.user and not request.user.is_superuser:
            return Response(
                {'detail': 'Você não tem permissão para finalizar este pedido.'},
                status=status.HTTP_403_FORBIDDEN
            )

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

        serializer = self.get_serializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def relatorio_vendas_mes(self, request):
        agora = timezone.now()
        inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        pedidos = Pedido.objects.filter(status=Pedido.StatusCompra.FINALIZADO, data__gte=inicio_mes)

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