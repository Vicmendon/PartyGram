from django.db import models
from evento.models import Festa

# Create your models here.
class Fornecedor(models.Model):
    ESTADO_SIGLA = [
        ('RJ', 'RJ'),
        ('SP', 'SP'),
        ('MG', 'MG'),
        ('ES', 'ES')

    ]

    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADO_SIGLA)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True, blank=True)


class Custo(models.Model):
    CUSTO_TIPO = [
        ('convidado', 'Por Convidado'),
        ('unico', 'Único'),
        ('hora', 'Por Hora')
    ]

    festa = models.ForeignKey(Festa, related_name='custos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=CUSTO_TIPO)
    fornecedor = models.ForeignKey(Fornecedor, related_name='custos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    def calcular_custo_por_convidado(self, num_convidados):
        if self.tipo == 'convidado':
            return self.valor * num_convidados
        elif self.tipo == 'hora':
            return self.valor * Festa.horas
        return self.valor

