from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from users.models import User
from django.http import JsonResponse

class HomePage(View):
    template_name = "home.html"
    def get(self, request):
        """ pagina inicial do projeto """
        return render(request, self.template_name)

def index(request):
    return redirect('home')