from django.db import models
from core.models.pedido.pedido import Pedido
from core.models.produto.produto import Produto

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens', verbose_name='Pedido')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name='Produto', related_name='itens')
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade', default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def total(self):
        return self.preco * self.quantidade


    def __str__(self):
        return f"{self.pedido} - {self.produto} - {self.quantidade}"