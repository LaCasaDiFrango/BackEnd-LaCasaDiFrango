from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer, CharField, SerializerMethodField,
    CurrentUserDefault, DateTimeField, IntegerField
)
from core.models.pedido.pedido import Pedido
from core.models.produto.produto import Produto
from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import (
    ItemPedidoSerializer, ItemPedidoCreateUpdateSerializer
)
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()


class PedidoSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=False)
    data_de_retirada = DateTimeField(read_only=True)
    itens = ItemPedidoSerializer(many=True, read_only=True)
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.total

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'status', 'total', 'itens', 'data_de_retirada', 'identificador')


class PedidoCreateUpdateSerializer(ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=CurrentUserDefault()
    )
    itens = ItemPedidoCreateUpdateSerializer(many=True, required=False)
    status = IntegerField(required=False, default=Pedido.StatusCompra.CARRINHO)
    identificador = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Pedido
        fields = ('usuario', 'itens', 'status', 'identificador')

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop('itens', [])
        usuario = validated_data.pop('usuario', None)
        status = validated_data.pop('status', Pedido.StatusCompra.CARRINHO)
        identificador = validated_data.pop('identificador', None)

        if usuario is None:
            usuario = self.context['request'].user

        # Cria o pedido inicialmente
        pedido = Pedido.objects.create(
            usuario=usuario,
            status=status,
            identificador=identificador,
            **validated_data
        )

        # Gera identificador automático se estiver vazio
        if not pedido.identificador:
            pedido.identificador = f"Pedido #{pedido.id}"
            pedido.save(update_fields=["identificador"])

        # Cria os itens do pedido
        for item in itens:
            produto_obj = item['produto']
            if not isinstance(produto_obj, Produto):
                produto_obj = Produto.objects.get(
                    pk=produto_obj.id if hasattr(produto_obj, 'id') else produto_obj
                )

            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto_obj,
                quantidade=item['quantidade'],
                preco=produto_obj.preco
            )

        # Atualiza o total do pedido
        pedido.total = sum(i.produto.preco * i.quantidade for i in pedido.itens.all())
        pedido.save(update_fields=["total", "identificador"])
        return pedido

    @transaction.atomic
    def update(self, pedido, validated_data):
        itens = validated_data.pop('itens', [])
        identificador = validated_data.pop('identificador', None)

        pedido_atualizado = super().update(pedido, validated_data)

        # Atualiza identificador (mantém ou gera se vazio)
        if identificador is not None:
            pedido_atualizado.identificador = identificador or f"Pedido #{pedido_atualizado.id}"

        if itens:
            pedido_atualizado.itens.all().delete()
            for item in itens:
                produto_obj = item['produto']
                if not isinstance(produto_obj, Produto):
                    produto_obj = Produto.objects.get(
                        pk=produto_obj.id if hasattr(produto_obj, 'id') else produto_obj
                    )
                ItemPedido.objects.create(
                    pedido=pedido_atualizado,
                    produto=produto_obj,
                    quantidade=item['quantidade'],
                    preco=produto_obj.preco
                )

        pedido_atualizado.total = sum(i.quantidade * i.preco for i in pedido_atualizado.itens.all())
        pedido_atualizado.save(update_fields=["total", "identificador"])
        return pedido_atualizado


class PedidoListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItemPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'itens', 'status')
