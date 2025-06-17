from rest_framework.viewsets import ModelViewSet

from core.models.pagamento.pagamento import Pagamento
from core.serializers.pagamento.pagamento import PagamentoSerializer

class PagamentoViewSet(ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer