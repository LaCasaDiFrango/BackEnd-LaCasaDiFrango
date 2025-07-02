from rest_framework.viewsets import ModelViewSet

from core.models.pedido.pedido import Pedido
from core.serializers.pedido.pedido import PedidoSerializer, PedidoCreateUpdateSerializer, PedidoListSerializer

class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PedidoListSerializer
        if self.action in ('create', 'update'):
            return PedidoCreateUpdateSerializer
        return PedidoSerializer

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Pedido.objects.all()
        if usuario.groups.filter(name='administradores').exists():
            return Pedido.objects.all()
        return Pedido.objects.filter(usuario=usuario)