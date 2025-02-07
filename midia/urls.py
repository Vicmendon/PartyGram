from django.urls import path
from .views import upload_arquivos

urlpatterns = [
    path('evento/<str:hash_evento>/upload/', upload_arquivos, name='upload'),

]
