from rest_framework.serializers import (ModelSerializer, CharField, SerializerMethodField, CurrentUserDefault, HiddenField, DateTimeField, IntegerField)
from core.models.pedido.pedido import Pedido
from core.models.produto.produto import Produto
from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import (ItemPedidoSerializer, ItemPedidoCreateUpdateSerializer, ItemPedidoListSerializer)
from django.db import transaction

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
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItemPedidoCreateUpdateSerializer(many=True, required=False)
    status = IntegerField(required=False, default=Pedido.StatusCompra.CARRINHO)

    class Meta:
        model = Pedido
        fields = ('usuario', 'itens', 'status')

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop('itens')
        usuario = validated_data['usuario']
        validated_data.pop('status', None)

        pedido, criado = Pedido.objects.get_or_create(
            usuario=usuario,
            status=Pedido.StatusCompra.CARRINHO,
            defaults=validated_data
        )

        for item in itens:
            produto_obj = item['produto']
            if not isinstance(produto_obj, Produto):
                produto_obj = Produto.objects.get(pk=produto_obj.id if hasattr(produto_obj, 'id') else produto_obj)

            item_existente = pedido.itens.filter(produto=produto_obj).first()
            if item_existente:
                item_existente.quantidade += item['quantidade']
                item_existente.save()
            else:
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto_obj,
                    quantidade=item['quantidade'],
                    preco=produto_obj.preco
                )

        pedido.total = sum(i.produto.preco * i.quantidade for i in pedido.itens.all())
        pedido.save()

        return pedido


    @transaction.atomic
    def update(self, pedido, validated_data):
        itens = validated_data.pop('itens', [])

    # Atualiza o pedido com os dados (menos os itens)
        pedido_atualizado = super().update(pedido, validated_data)

        if itens:
            pedido_atualizado.itens.all().delete()
            for item in itens:
                produto_obj = item['produto']
                if not isinstance(produto_obj, Produto):
                    produto_obj = Produto.objects.get(pk=produto_obj.id if hasattr(produto_obj, 'id') else produto_obj)

                item['preco'] = produto_obj.preco
                item['produto'] = produto_obj
                ItemPedido.objects.create(pedido=pedido_atualizado, **item)

        pedido_atualizado.save()
        return pedido_atualizado



class PedidoListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItemPedidoSerializer(many=True, read_only=True)  # aqui o produto vai vir completo

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'itens', 'status')  # inclua status se quiser mostrar
