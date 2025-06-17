from django.db import models

from core.models.pedido.pedido import Pedido
from core.models.produto.produto import Produto

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, verbose_name='Pedido')
    produto = models.ForeignKey('Produto', on_delete=models.PROTECT, verbose_name='Produto')
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade', default=1)



    def __str__(self):
        return f"{self.pedido} - {self.produto} - {self.quantidade}"