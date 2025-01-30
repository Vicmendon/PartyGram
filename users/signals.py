from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import User
from decouple import config  # ou from dotenv import load_dotenv, dotenv_values

@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    """Cria um superusuário padrão se ele ainda não existir"""
    if not User.objects.filter(username=config('DEFAULT_USER_USERNAME')).exists():
        User.objects.create_superuser(
            username=config('DEFAULT_USER_USERNAME'),
            email=config('DEFAULT_USER_EMAIL'),
            password=config('DEFAULT_USER_PASSWORD')
        )
        print("Superusuário padrão criado com sucesso!")