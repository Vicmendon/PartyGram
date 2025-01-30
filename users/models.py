from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField()
    telefone = models.CharField(max_length=11)
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
