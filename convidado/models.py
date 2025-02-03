from django.db import models


class Convidado(models.Model):
    RSVP_CHOICES = [
        ('SIM', 'Vai'),
        ('NÃO', 'Não vai'),
        ('IND', 'Indefinido')
    ]

    evento = models.ForeignKey('evento.Festa', related_name='convidados', on_delete=models.CASCADE)
    telefone = models.CharField(max_length=11, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    cervejeiro = models.BooleanField(default=False)
    rsvp = models.CharField(max_length=3, choices=RSVP_CHOICES, default='IND')
    convite_enviado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


class Parente(models.Model):
    RSVP_CHOICES = [
        ('SIM', 'Vai'),
        ('NAO', 'Não vai'),
        ('IND', 'Indefinido')
    ]
    
    IDADE_CHOICES = [
        ('AD', 'Adulto'),
        ('CR', 'Criança'),
        ('BB', 'Bebê')
    ]

    convidado = models.ForeignKey(Convidado, related_name='parentes', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    idade = models.CharField(max_length=2, choices=IDADE_CHOICES, default='AD')
    cervejeiro = models.BooleanField(default=False)
    rsvp = models.CharField(max_length=3, choices=RSVP_CHOICES, default='IND')

    def __str__(self):
        return f'{self.nome} ({self.convidado})'


class ErroConfirmacao(models.Model):
    nome_incorreto = models.CharField(max_length=100)
    numero_whatsapp_incorreto = models.CharField(max_length=11)
    link = models.URLField()  # URL que o convidado recebe, oculta nesse formulário
    criado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Erro de confirmação para {self.nome_incorreto} ({self.numero_whatsapp_incorreto})'


class LogEventos(models.Model):
    usuario = models.ForeignKey(Convidado, on_delete=models.CASCADE)
    hora = models.DateTimeField(auto_now=True)
    registro = models.CharField(max_length=200)

    def __str__(self):
        return f'Log para {self.usuario} em {self.hora}'
