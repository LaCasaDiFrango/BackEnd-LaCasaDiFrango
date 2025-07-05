from rest_framework.serializers import (ModelSerializer, CharField, SerializerMethodField, CurrentUserDefault, HiddenField, DateTimeField)
from core.models.pedido.pedido import Pedido
from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import (ItemPedidoSerializer, ItemPedidoCreateUpdateSerializer, ItemPedidoListSerializer)
from django.db import transaction

class PedidoSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    data_de_retirada = DateTimeField(read_only=True)
    itens = ItemPedidoSerializer(many=True, read_only=True)
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.total

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'status', 'total', 'itens', 'data_de_retirada')


class PedidoCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItemPedidoCreateUpdateSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ('usuario', 'itens')

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop('itens')
        usuario = validated_data['usuario']

        pedido, criado = Pedido.objects.get_or_create(
            usuario=usuario,
            status=Pedido.StatusCompra.CARRINHO,
            defaults=validated_data
        )

        for item in itens:
            item_existente = pedido.itens.filter(produto=item['produto']).first()

            if item_existente:
                item_existente.quantidade += item['quantidade']
                item_existente.preco = item['produto'].preco
                item_existente.save()
            else:
                item['preco'] = item['produto'].preco
                ItemPedido.objects.create(pedido=pedido, **item)

        pedido.save()

        return pedido

    @transaction.atomic
    def update(self, pedido, validated_data):
        itens = validated_data.pop('itens', [])

        if itens:
            pedido.itens.all().delete()
            for item in itens:
                item['preco'] = item['produto'].preco
                ItemPedido.objects.create(pedido=pedido, **item)

        pedido.save()

        return super().update(pedido, validated_data)


class PedidoListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItemPedidoListSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'itens')
