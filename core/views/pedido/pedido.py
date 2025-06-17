from rest_framework.viewsets import ModelViewSet

from core.models.pedido.pedido import Pedido
from core.serializers.pedido.pedido import PedidoSerializer

class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer