from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from users.models import User
from django.http import JsonResponse

class AuthLogin(View):
    template_name = "login.html"
    def get(self, request):
        try:
            """Se o usuário já estiver autenticado, redireciona para home ou para a página next"""
            if request.user.is_authenticated:
                next_url = request.GET.get("next") or "home"
                return redirect(next_url)
        except Exception as e:
            print(e)
            
        return render(request, self.template_name)

    def post(self, request):
        """Autentica o usuário e redireciona para a página desejada"""
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        user = authenticate(request, email=email, password=senha)

        if user:
            login(request, user)
            next_url = request.GET.get("next") or "home"
            return redirect(next_url)
        else:
            messages.error(request, "E-mail ou senha inválidos")
            return render(request, self.template_name)
    
class AuthLogout(View):
    def get(self, request):
        """Desloga o usuário e o redireciona para a página inicial"""
        logout(request)
        return redirect(reverse_lazy("home"))

class AuthRegister(View):
    def post(self, request):
        """Registra um novo usuário se o e-mail ainda não estiver cadastrado"""
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")

        # Verifica se já existe um usuário com o mesmo e-mail
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Este e-mail já está cadastrado."}, status=400)
        
        # Cria o usuário com senha criptografada
        user = User.objects.create_user(nome=nome, sobrenome=sobrenome, email=email, password=senha)
        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect('home')