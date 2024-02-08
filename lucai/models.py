from django.db import models

# Create your models here.
# models.py

from django.db import models

from django.db import models

from django.db import models

class Transacao(models.Model):
    DESPESA = 'despesa'
    RECEITA = 'receita'

    TIPO_CHOICES = [
        (DESPESA, 'Despesa'),
        (RECEITA, 'Receita'),
    ]

    CATEGORIAS_CHOICES = [
        ('Salário', 'Salário'),
        ('Contas', 'Contas em geral'),
        ('Aluguel', 'Aluguel'),
        ('Cartão de Crédito', 'Cartão de Crédito'),
        ('Empréstimos', 'Empréstimos'),
        ('Entretenimento', 'Entretenimento'),
        ('Outros', 'Outros'),
    ]

    descricao = models.CharField(max_length=100, choices=CATEGORIAS_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} - {self.valor} - {self.get_tipo_display()} - {self.data}"




