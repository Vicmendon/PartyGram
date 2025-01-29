# from django.urls import path
# from . import views
#
#
# urlpatterns = [
#     path('confirmar-presenca/<str:link_identificador>/', views.confirmar_presenca, name='confirmar_presenca'),
#     path('confirmacao/<int:convidado_id>', views.confirmacao, name='confirmacao'),
#     path('erro/', views.erro_confirmacao, name='erro_confirmacao'),
# ]

from django.urls import path
from .views import confirma_presenca

urlpatterns = [
    # path('evento/<int:evento_id>/confirmacao/', confirma_presenca, name='confirma_presenca'),
    path('evento/<str:hash_evento>/confirmacao/', confirma_presenca, name='confirma_presenca'),
]
