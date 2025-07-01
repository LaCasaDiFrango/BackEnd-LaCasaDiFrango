from django.db import models

from core.models.usuario.user import User
from rest_framework.serializers import CharField, ModelSerializer

class Pedido(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        FINALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"

    data_de_retirada = models.DateTimeField(verbose_name='Data de Validade do Pedido', auto_now_add=True)
    status = CharField(source='get_status_display', read_only=True)
    usuario = CharField(source='usuario.e-mail', read_only=True)


    def __str__(self):
        return f"{self.data_de_retirada} - {self.status}"