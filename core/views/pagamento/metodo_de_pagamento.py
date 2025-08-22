from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser, IsGuestOrReadOnly
from rest_framework.viewsets import ModelViewSet

from core.models.pagamento.metodo_de_pagamento import MetodoDePagamento
from core.serializers.pagamento.metodo_de_pagamento import MetodoDePagamentoSerializer


class MetodoDePagamentoViewSet(ModelViewSet):
    queryset = MetodoDePagamento.objects.all()
    serializer_class = MetodoDePagamentoSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        if self.action in ['list', 'retrieve']:
            return [IsGuestOrReadOnly()]
        return super().get_permissions()
