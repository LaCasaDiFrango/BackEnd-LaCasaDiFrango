from django.db import models
from core.models.usuario.user import User

class Pedido(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        FINALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"

    # 🆕 Campo para registrar quando o pedido foi criado
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação do pedido')

    # Campo já existente, mantém sua função original
    data_de_retirada = models.DateTimeField(verbose_name='Data de Retirada do Pedido', auto_now_add=True)

    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pedidos', null=True, blank=True)
    identificador = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
