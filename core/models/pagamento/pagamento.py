from django.db import models
from core.models.pedido.pedido import Pedido
from core.models.pagamento.metodo_de_pagamento import MetodoDePagamento

class Pagamento(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, verbose_name='Pedido')
    metodo_de_pagamento = models.ForeignKey('MetodoDePagamento', on_delete=models.PROTECT, verbose_name='Método de Pagamento', null=True, blank=True)

    def __str__(self):
        return f"{self.pedido}"