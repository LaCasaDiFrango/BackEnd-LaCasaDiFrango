from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from core.models.pedido.pedido import Pedido
from core.models.pedido.item_pedido import ItemPedido
from core.serializers.pedido.item_pedido import ItemPedidoSerializer, ItemPedidoCreateUpdateSerializer

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
    itens = ItemPedidoCreateUpdateSerializer(many=True) # Aqui mudou

    class Meta:
        model = Pedido
        fields = ('usuario', 'itens')

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item_data in itens_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)
        pedido.save()
        return pedido
