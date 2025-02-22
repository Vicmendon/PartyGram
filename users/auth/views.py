from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from users.models import User
from django.http import JsonResponse
import random
import string
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from django.core import signing
import json

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
            lembre = request.POST.get("lembre") == "on"

            if not lembre:
                request.session.set_expiry(0)  # Expira ao fechar a guia
                request.session.flush()  # Remove todos os dados da sessão
                print("Sessão configurada para expirar ao fechar o navegador.")
            else:
                request.session.set_expiry(1209600)  # 2 semanas
                print("Sessão configurada para durar 2 semanas.")
            login(request, user)
            return JsonResponse({"success": True, "message": "Acessando sua conta..."}, status=200)
        else:
           return JsonResponse({"success": False, "message": "Credenciais inválidas"}, status=400)
    
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
        print(email, senha, nome, sobrenome)
        # Verifica se já existe um usuário com o mesmo e-mail
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Este e-mail já está cadastrado."}, status=400)
        
        # Cria o usuário com senha criptografada
        user = User.objects.create_user(username=email, nome=nome, sobrenome=sobrenome, email=email, password=senha)
        user = authenticate(request, email=email, password=senha)
        login(request, user)
        return JsonResponse({"success": True, "message": "Conta criada com sucesso!"}, status=200)
    
class AuthForgotPassword(View):
    def get(self, request):
        if request.user.is_authenticated:
            next_url = request.GET.get("next") or "home"
            return redirect(next_url)
        return render(request, "esqueceu_senha.html")
    
    def post(self, request):
        try:
            email = request.POST.get("email")
            if not User.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "message": "Este e-mail não foi encontrado."}, status=400)
            
            # Verifica se já existe um código para esse e-mail e remove
            cache_key = f"codigo_verificacao_{email}"
            codigo_existente = cache.get(cache_key)
            print(codigo_existente)
            if codigo_existente:
                cache.delete(cache_key)

            # Gera um novo código aleatório de 6 dígitos
            novo_codigo = ''.join(random.choices(string.digits, k=6))

            # Armazena o código no cache com duração de 10 minutos (600 segundos)
            cache.set(cache_key, novo_codigo, timeout=600)
            
            # envio de email para o usuario
            send_mail(
                subject="Codigo de Recuperação",
                message=f"Seu codigo de Recuperação é: {novo_codigo}",
                from_email="starseguro.sistemas@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
            
            return JsonResponse({"success": True, "message": "Um código foi enviado para o seu e-mail."}, status=200)
            
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    
    def put(self, request):
        try:
            data = json.loads(request.body)
            email = data.get("email")
            codigo = data.get("code")
            if not email:
                return JsonResponse({"success": False, "message": "Houve um erro ao buscar seu E-mail."}, status=400)
            
            # Verifica se é um codigo valido
            cache_key = f"codigo_verificacao_{email}"
            codigo_existente = cache.get(cache_key)
            print(codigo_existente)
            
            if not codigo_existente:
                return JsonResponse({"success": False, "message": "Seu codigo de Recuperação expirou. Tente novamente."}, status=400)
            
            if codigo == codigo_existente:
                dados = {"email": email, "codigo": codigo}
                hash_code = signing.dumps(dados, salt=settings.SECRET_KEY)
                return JsonResponse({"success": True, "message": "Codigo validado! Redirecionando para tela de alteração de senha.", "hash": hash_code}, status=200)
            
            return JsonResponse({"success": False, "message": "O Código informado é inválido. Tente novamente."}, status=400)
            
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": str(e)}, status=500)
        
class AuthRecovery(View):
    def get(self, request, hash_code):
        try:
            if request.user.is_authenticated:
                next_url = request.GET.get("next") or "home"
                return redirect(next_url)
            
            dados = signing.loads(hash_code, salt=settings.SECRET_KEY)
            email = dados.get("email")
            codigo = dados.get("codigo")
            cache_key = f"codigo_verificacao_{email}"
            codigo_existente = cache.get(cache_key)
            if not codigo_existente:
                messages.error(request, "Seu codigo de Recuperação expirou. Tente novamente.")
                return redirect('login')
            
            if codigo != codigo_existente:
                messages.error(request, "O Código informado é inválido. Tente novamente.")
                return redirect('login')
            
            return render(request, "recuperar_senha.html", {"hash": hash_code})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    
class AuthRChagePassword(View):
    def post(self, request):
        try:
            if request.user.is_authenticated:
                next_url = request.GET.get("next") or "home"
                return redirect(next_url)
            
            hash_code = request.POST.get("hash_code")
            dados = signing.loads(hash_code, salt=settings.SECRET_KEY)
            email = dados.get("email")
            
            user = User.objects.get(email=email)
            if not user:
                JsonResponse({"success": False, "message": "Conta nao encontrada."}, status=400)
            
            senha = request.POST.get("senha")
            user.set_password(senha)
            user.save()
            
            return JsonResponse({"success": True, "message": "Senha alterada com sucesso!"}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": str(e)}, status=500)
            
                
                
    