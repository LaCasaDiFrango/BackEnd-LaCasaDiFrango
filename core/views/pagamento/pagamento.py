from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from core.models.pagamento.pagamento import Pagamento
from core.serializers.pagamento.pagamento import PagamentoSerializer


class PagamentoViewSet(ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]  # consumidor pode pagar
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]  # só admins acessam pagamentos de todos
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='administradores').exists() or user.is_superuser:
            return Pagamento.objects.all()
        return Pagamento.objects.filter(usuario=user)
