from rest_framework.viewsets import ModelViewSet

from core.models.pagamento.metodo_de_pagamento import MetodoDePagamento
from core.serializers.pagamento.metodo_de_pagamento import MetodoDePagamentoSerializer

class MetodoDePagamentoViewSet(ModelViewSet):
    queryset = MetodoDePagamento.objects.all()
    serializer_class = MetodoDePagamentoSerializer