from django.db import models
from core.models.pedido.pedido import Pedido

class Pagamento(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, verbose_name='Pedido')

    def __str__(self):
        return f"{self.pedido}"