from django.db import models

class Produto(models.Model):
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço', default=0.00)
    nome = models.CharField(max_length=100, verbose_name='Nome do Produto', default="")
    descricao = models.TextField(verbose_name='Descrição do Produto', default="")
    quantidade_em_estoque = models.PositiveIntegerField(verbose_name='Quantidade em Estoque', default=0)
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, null=True, blank=True, related_name='produtos', verbose_name='Categoria', help_text='Categoria do produto')
    imagem_url = models.URLField(max_length=500, blank=True, null=True)  


    def __str__(self):
        return f"{self.nome} - {self.preco}"