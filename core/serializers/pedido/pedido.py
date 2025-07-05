from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, CurrentUserDefault, HiddenField
from core.models.pedido.pedido import Pedido
from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import ItemPedidoSerializer, ItemPedidoCreateUpdateSerializer, ItemPedidoListSerializer

class PedidoSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    itens = ItemPedidoSerializer(many=True, read_only=True)
    total = SerializerMethodField()

    def get_total(self, instance):
        return sum(item.produto.preco * item.quantidade for item in instance.itens.all())

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'status', 'total', 'itens')

class PedidoCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItemPedidoCreateUpdateSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ('usuario', 'itens')

    def create(self, validated_data):
        itens = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item in itens:
            item['preco'] = item['produto'].preco # nova linha
            ItemPedido.objects.create(pedido=pedido, **item)
        pedido.save()
        return pedido

class PedidoListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItemPedidoListSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'itens')
