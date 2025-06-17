from django.db import models
from core.models.usuario.cartao import Cartao

class MetodoDePagamento(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.PROTECT, verbose_name='Cartao', null=True, blank=True)

    def __str__(self):
        return f"{self.cartao}"