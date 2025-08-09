from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone

from core.models.pedido.pedido import Pedido
from core.models.produto.produto import Produto
from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.pedido import (
    PedidoSerializer,
    PedidoCreateUpdateSerializer,
    PedidoListSerializer
)

from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser, IsOwnerOrAdmin

class PedidoViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return PedidoListSerializer
        if self.action == 'retrieve':
            return PedidoSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return PedidoCreateUpdateSerializer
        return PedidoSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        if self.action in ['relatorio_vendas_mes', 'remover_item']:
            return [IsAuthenticated(), IsAdminUser()]
        if self.action in ['finalizar', 'adicionar_item']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser or usuario.groups.filter(name='administradores').exists():
            return Pedido.objects.all().order_by('-data_de_retirada')
        return Pedido.objects.filter(usuario=usuario).order_by('-data_de_retirada')

    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        pedido = self.get_object()

        if pedido.usuario != request.user and not request.user.is_superuser:
            return Response(
                {'detail': 'Você não tem permissão para finalizar este pedido.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if pedido.status != Pedido.StatusCompra.CARRINHO:
            return Response(
                {'status': 'pedido já finalizado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            for item in pedido.itens.all():
                if item.quantidade > item.produto.quantidade_em_estoque:
                    return Response(
                        {
                            'status': 'Quantidade insuficiente',
                            'produto': item.produto.nome,
                            'quantidade_disponivel': item.produto.quantidade_em_estoque,
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                item.produto.quantidade_em_estoque -= item.quantidade
                item.produto.save()

            pedido.status = Pedido.StatusCompra.FINALIZADO
            pedido.save()

        serializer = self.get_serializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def relatorio_vendas_mes(self, request):
        agora = timezone.now()
        inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        pedidos = Pedido.objects.filter(
            status=Pedido.StatusCompra.FINALIZADO,
            data__gte=inicio_mes
        )

        total_vendas = sum(pedido.total for pedido in pedidos)
        quantidade_vendas = pedidos.count()

        return Response(
            {
                'status': 'Relatório de vendas deste mês',
                'total_vendas': total_vendas,
                'quantidade_vendas': quantidade_vendas,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def adicionar_item(self, request, pk=None):
        pedido = self.get_object()

        if pedido.status != Pedido.StatusCompra.CARRINHO:
            return Response(
                {'detail': 'Não é possível adicionar itens a um pedido finalizado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        produto_id = request.data.get("produto_id")
        quantidade = request.data.get("quantidade", 1)

        if not produto_id:
            return Response({'detail': 'Produto não informado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            produto = Produto.objects.get(pk=produto_id)
        except Produto.DoesNotExist:
            return Response({'detail': 'Produto não encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)

        item_existente = pedido.itens.filter(produto=produto).first()

        if item_existente:
            item_existente.quantidade += int(quantidade)
            item_existente.save()
        else:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=int(quantidade),
                preco=produto.preco
            )

        pedido.total = sum(i.quantidade * i.preco for i in pedido.itens.all())
        pedido.save()

        return Response({'detail': 'Item adicionado com sucesso.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"])
    def remover_item(self, request, pk=None):
        pedido = self.get_object()

        if pedido.status != Pedido.StatusCompra.CARRINHO:
            return Response(
                {'detail': 'Não é possível remover itens de um pedido finalizado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        produto_id = request.data.get("produto_id")

        if not produto_id:
            return Response({'detail': 'Produto não informado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        item = pedido.itens.filter(produto_id=produto_id).first()

        if not item:
            return Response({'detail': 'Item não encontrado no pedido.'},
                            status=status.HTTP_404_NOT_FOUND)

        item.delete()

        pedido.total = sum(i.quantidade * i.preco for i in pedido.itens.all())
        pedido.save()

        return Response({'detail': 'Item removido com sucesso.'}, status=status.HTTP_200_OK)
