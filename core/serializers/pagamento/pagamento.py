from rest_framework.serializers import ModelSerializer

from core.models.pagamento.pagamento import Pagamento

class PagamentoSerializer(ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'
        depth = 1
