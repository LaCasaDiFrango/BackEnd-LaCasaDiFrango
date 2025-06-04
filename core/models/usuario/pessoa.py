from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=45, verbose_name='Nome')
    email = models.EmailField(max_length=254, unique=True, verbose_name='Email')
    telefone = models.CharField(max_length=20, verbose_name='Telefone', blank=True, null=True)
    endereco = models.ForeignKey('core.Endereco', on_delete=models.PROTECT, verbose_name='Endereço', null=True, blank=True)
    cartao = models.ForeignKey('core.Cartao', on_delete=models.PROTECT, verbose_name='Cartão', null=True, blank=True)

    def __str__(self):
        return self.nome
