from rest_framework.viewsets import ModelViewSet

from core.models.pedido.pedido import Pedido
from core.serializers.pedido.pedido import PedidoSerializer, PedidoCreateUpdateSerializer

class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return PedidoCreateUpdateSerializer
        return PedidoSerializer