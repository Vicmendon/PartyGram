from django.urls import path
from .views import visualizar_galeria
from midia.views import upload_arquivos

urlpatterns = [
    #path('<str:hash_evento>/media', visualizar_uploads, name='upload'),
    path('<str:hash_evento>/galeria', visualizar_galeria, name='galeria'),
    path('<str:hash_evento>/upload/', upload_arquivos, name='upload'),
]
