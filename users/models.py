from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField()
    telefone = models.CharField(max_length=11)
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
