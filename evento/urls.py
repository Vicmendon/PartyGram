from django.urls import path
from .views import visualizar_galeria
from midia.views import upload_arquivos, remove_media

app_name = 'evento'  # Defina o namespace do app aqui

urlpatterns = [
    path('<str:hash_evento>/remove_media/<str:media_type>/<int:media_id>/', remove_media, name='remove_media'),
    path('<str:hash_evento>/galeria', visualizar_galeria, name='galeria'),
    path('<str:hash_evento>/upload/', upload_arquivos, name='upload'),
]