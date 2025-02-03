from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import User
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    """Cria um superusuário padrão se ele ainda não existir"""
    if not User.objects.filter(username=os.getenv('DEFAULT_USER_USERNAME')).exists():
        User.objects.create_superuser(
            username=os.getenv('DEFAULT_USER_USERNAME'),
            email=os.getenv('DEFAULT_USER_EMAIL'),
            password=os.getenv('DEFAULT_USER_PASSWORD')
        )
        print("Superusuário padrão criado com sucesso!")