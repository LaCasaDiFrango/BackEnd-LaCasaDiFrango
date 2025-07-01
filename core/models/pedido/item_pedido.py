from django.db import models
from core.models.pedido.pedido import Pedido
from core.models.produto.produto import Produto

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens', verbose_name='Pedido')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name='Produto', related_name='itens')
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade', default=1)

    @property
    def total(self):
        # total = 0
        # for item in self.itens.all():
        #     total += item.produto.preco * item.quantidade
        # return total
        return sum(item.produto.preco * item.quantidade for item in self.itens.all())


    def __str__(self):
        return f"{self.pedido} - {self.produto} - {self.quantidade}"