from django.db import models

from core.models.usuario.user import User

class Pedido(models.Model):
    preco_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Total do Pedido', default=0.00)
    data_de_retirada = models.DateTimeField(verbose_name='Data de Validade do Pedido', auto_now_add=True)
    status = models.CharField(max_length=20, verbose_name='Status do Pedido', default='Pendente')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuário do Pedido', null=True, blank=True)



    def __str__(self):
        return f"{self.data_de_retirada} - {self.status}"