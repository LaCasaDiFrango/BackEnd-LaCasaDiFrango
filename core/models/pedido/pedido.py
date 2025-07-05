from django.db import models
from core.models.usuario.user import User

class Pedido(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        FINALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"

    data_de_retirada = models.DateTimeField(verbose_name='Data de Validade do Pedido', auto_now_add=True)
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pedidos', null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # novo campo

    def __str__(self):
        return f"{self.data_de_retirada} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        self.total = sum(item.preco * item.quantidade for item in self.itens.all())
        super().save(*args, **kwargs)
