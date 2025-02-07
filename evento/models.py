from django.db import models
from users.models import User
from django.db.models import Count
from convidado.models import Convidado
import random
import string


# Create your models here.
def gerar_hash_evento():
    while True:
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not Festa.objects.filter(hash_evento=codigo).exists():
            return codigo

class Festa(models.Model):
    ESTADO_CHOICES = [
        ('RJ', 'RJ')
    ]

    hash_evento = models.CharField(max_length=20, default=gerar_hash_evento)
    organizador = models.ForeignKey(User, related_name='festas', on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    data = models.DateTimeField()
    horas = models.DecimalField(max_digits=2, decimal_places=0, default=4)
    descricao = models.TextField()
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, default='RJ')
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    compl_endereco = models.CharField(max_length=300, null=True, blank=True)
    GPS = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'

    def total_convidados(self):
        return self.convidados.count() + sum([convidado.parentes.count() for convidado in self.convidados.all()])

    def total_confirmados(self):
        convidados_confirmados = self.convidados.filter(rsvp='SIM')
        return sum([1 for convidado in convidados_confirmados] + [1 for convidado in convidados_confirmados for parente in convidado.parentes.filter(convidado__rsvp='SIM')])
    
    def total_recusaram(self):
        convidados_recusaram = self.convidados.filter(rsvp="NÃO")
        return sum([1 for convidado in convidados_recusaram] + [1 for convidado in convidados_recusaram for parente in convidado.parentes.filter(convidado__rsvp='NÃO')])

    def total_cervejeiros(self):
        convidados_cervejeiros = self.convidados.filter(cervejeiro=True)
        return sum([1 for convidado in convidados_cervejeiros] + [1 for convidado in convidados_cervejeiros for parente in convidado.parentes.filter(convidado__cervejeiro=True)])
