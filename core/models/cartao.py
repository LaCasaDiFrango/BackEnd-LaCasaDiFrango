from django.db import models

class Cartao(models.Model):
    nome_titular = models.CharField(max_length=45, verbose_name='Nome do Titular', default="")
    numero_cartao = models.CharField(max_length=20, verbose_name='Número do Cartão', default="")
    data_de_validade = models.CharField(max_length=7, verbose_name='Data de Validade', default="")
    cvv = models.CharField(max_length=4, verbose_name='CVV', default="")
    bandeira = models.CharField(max_length=20, verbose_name='Bandeira', default="")

    def __str__(self):
        return f"{self.nome_titular} - {self.bandeira}"