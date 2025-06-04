from django.db import models

class Endereco(models.Model):
    bairro = models.CharField(max_length=45, verbose_name='Bairro')
    rua = models.CharField(max_length=45, verbose_name='Rua')
    numero = models.CharField(max_length=10, verbose_name='Número')  # Pode ter letras
    cep = models.CharField(max_length=9, verbose_name='CEP', help_text='Formato: 99999-999')
    complemento = models.CharField(max_length=45, blank=True, null=True, verbose_name='Complemento')

    def __str__(self):
        parts = [self.bairro, self.rua, self.numero, self.cep]
        if self.complemento:
            parts.append(self.complemento)
        return ", ".join(parts)
