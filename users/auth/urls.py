from django.urls import path
from .views import *

urlpatterns = [
    path('login', AuthLogin.as_view(), name='login'),
    path('logout', AuthLogout.as_view(), name='logout'),
    path('register', AuthRegister.as_view(), name='register'),
    path('recovery', AuthForgotPassword.as_view(), name='recovery'),
    path('recovery/<str:hash_code>', AuthRecovery.as_view(), name='recovery-page'),
    path('chage-password', AuthRChagePassword.as_view(), name='chage-password'),
]
