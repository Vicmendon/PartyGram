from django.db import models
# from evento.models import Festa


# Create your models here.
class Convidado(models.Model):
    evento = models.ForeignKey('evento.Festa', related_name='convidados', on_delete=models.CASCADE)
    telefone = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    cervejeiro = models.BooleanField(default=False)
    rsvp = models.BooleanField(default=False)
    convite_enviado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


class Parente(models.Model):
    IDADE_CHOICES = [
        ('AD', 'Adulto'),
        ('CR', 'Criança'),
        ('BB', 'Bebê')
    ]

    convidado = models.ForeignKey(Convidado, related_name='parentes', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    idade = models.CharField(max_length=2, choices=IDADE_CHOICES, default='AD')
    cervejeiro = models.BooleanField(default=False)
    rsvp = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome} ({self.convidado})'


class ErroConfirmacao(models.Model):
    nome_incorreto = models.CharField(max_length=100)
    numero_whatsapp_incorreto = models.CharField(max_length=11)
    link = models.URLField()    # url que convidado recebe, oculta nesse formulário
    criado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Erro de confirmação para {self.nome_incorreto} ({self.numero_whatsapp_incorreto})'


class LogEventos(models.Model):
    usuario = models.ForeignKey(Convidado, on_delete=models.CASCADE, )
    hora = models.DateTimeField(auto_now=True)
    registro = models.CharField(max_length=200)


