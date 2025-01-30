from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# View para a página de login
class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True  # Redireciona se já estiver logado
    success_url = reverse_lazy("home")  # Para onde redirecionar após login

# View para a página inicial
class HomeView(TemplateView):
    template_name = "home.html"