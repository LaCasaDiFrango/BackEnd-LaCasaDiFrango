from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsAdminUser, IsConsumerUser, IsGuestOrReadOnly, IsOwnerOrAdmin, IsPedidoOwnerOrAdmin

from core.models.pagamento.pagamento import Pagamento
from core.serializers.pagamento.pagamento import PagamentoSerializer



class PagamentoViewSet(ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsPedidoOwnerOrAdmin()]
        return [IsAuthenticated()]
