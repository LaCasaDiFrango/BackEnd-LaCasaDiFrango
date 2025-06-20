from rest_framework.serializers import ModelSerializer

from core.models.pagamento.metodo_de_pagamento import MetodoDePagamento

class MetodoDePagamentoSerializer(ModelSerializer):
    class Meta:
        model = MetodoDePagamento
        fields = '__all__'
        depth = 1
