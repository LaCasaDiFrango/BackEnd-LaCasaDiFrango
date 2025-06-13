from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do Categoria', default="")
    descricao = models.TextField(verbose_name='Descrição do Categoria', default="")


    def __str__(self):
        return f"{self.nome} - {self.descricao}"