from django.db import models

class Pessoa(models.Model):
    nome= models.CharField(max_length=45, verbose_name='Nome', default="")
    email= models.EmailField(max_length=45, unique=True, verbose_name='Email', default='exemplo@gmail.com')
    telefone= models.CharField(max_length=20, verbose_name='Telefone', default="")
    endereco = models.ForeignKey('core.Endereco', on_delete=models.PROTECT, verbose_name='Endereço', null=True, blank=True)

    def __str__(self):
        return self.nome