from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from core.models.pedido.pedido import Pedido
from core.serializers.pedido.item_pedido import ItemPedidoSerializer

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
