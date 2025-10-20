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
        fields = ('id', 'usuario', 'status', 'total', 'itens', 'data_de_retirada')


class PedidoCreateUpdateSerializer(ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,  # opcional
        default=CurrentUserDefault()
    )
    itens = ItemPedidoCreateUpdateSerializer(many=True, required=False)
    status = IntegerField(required=False, default=Pedido.StatusCompra.CARRINHO)

    class Meta:
        model = Pedido
        fields = ('usuario', 'itens', 'status')

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop('itens', [])
        usuario = validated_data.pop('usuario', None)
        status = validated_data.pop('status', Pedido.StatusCompra.CARRINHO)

        # Se não passar usuário, pega o usuário autenticado
        if usuario is None:
            usuario = self.context['request'].user

        pedido = Pedido.objects.create(
            usuario=usuario,
            status=status,
            **validated_data
        )

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
        pedido.save()

        return pedido

    @transaction.atomic
    def update(self, pedido, validated_data):
        itens = validated_data.pop('itens', [])

        # Atualiza os campos restantes do pedido
        pedido_atualizado = super().update(pedido, validated_data)

        if itens:
            pedido_atualizado.itens.all().delete()
            for item in itens:
                produto_obj = item['produto']
                if not isinstance(produto_obj, Produto):
                    produto_obj = Produto.objects.get(
                        pk=produto_obj.id if hasattr(produto_obj, 'id') else produto_obj
                    )
                item['preco'] = produto_obj.preco
                item['produto'] = produto_obj
                ItemPedido.objects.create(pedido=pedido_atualizado, **item)

        pedido_atualizado.save()
        return pedido_atualizado


class PedidoListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItemPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'itens', 'status')
