from django.urls import path
from .views import *

urlpatterns = [
    path('login', AuthLogin.as_view(), name='login'),
    path('logout', AuthLogout.as_view(), name='logout'),
    path('register', AuthRegister.as_view(), name='register'),
]
