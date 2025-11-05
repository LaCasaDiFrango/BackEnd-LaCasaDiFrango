from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from core.models.usuario.user import User

class Pedido(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        FINALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"

    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação do pedido')
    data_de_retirada = models.DateTimeField(auto_now_add=True, verbose_name='Data de Retirada do Pedido')

    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pedidos', null=True, blank=True)
    identificador = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.get_status_display()}"

@receiver(post_save, sender=Pedido)
def atualizar_ultimo_pedido(sender, instance, created, **kwargs):
    """Atualiza o último pedido do usuário sempre que um pedido é criado ou atualizado"""
    if instance.usuario:
        # Usa timezone.localtime para garantir que seja comparável
        ultimo = instance.usuario.ultimo_pedido
        pedido_aware = timezone.localtime(instance.data_de_retirada)
        if not ultimo or pedido_aware > timezone.localtime(ultimo):
            instance.usuario.ultimo_pedido = pedido_aware
            instance.usuario.save()
