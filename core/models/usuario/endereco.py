from django.db import models

class Endereco(models.Model):
    bairro = models.CharField(max_length=45, verbose_name='Bairro', default="")
    rua = models.CharField(max_length=45, verbose_name='Rua', default="")
    numero = models.CharField(max_length=10, verbose_name='Número', default="")
    cep = models.CharField(max_length=10, verbose_name='CEP', default="")
    complemento = models.CharField(max_length=45, blank=True, null=True, verbose_name='Complemento', default="")

    def __str__(self):
        return f"{self.bairro}, {self.rua}, {self.numero}, {self.cep}, {self.complemento}"