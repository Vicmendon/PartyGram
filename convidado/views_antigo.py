from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Convidado, ErroConfirmacao
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


def confirmar_presenca(request, link_identificador):
    if request.method == 'POST':
        numero_whatsapp = request.POST.get('numero_whatsapp')
        primeiro_nome = request.POST.get('primeiro_nome')

        try:
            convidado = Convidado.objects.get(telefone=numero_whatsapp, nome=primeiro_nome)
            return redirect('confirmacao', convidado_id=convidado.id)

        except ObjectDoesNotExist:
            erro_link = f"{request.build_absolute_uri(reverse('confirmar_presenca', args=[link_identificador]))}"
            ErroConfirmacao.objects.create(
                nome_incorreto=primeiro_nome,
                numero_whatsapp_incorreto=numero_whatsapp,
                link=erro_link
            )
            return redirect('erro_confirmacao')

    return render(request, 'convidado/formulario_confirmacao.html', {'link_identificador': link_identificador})


def confirmacao(request, convidado_id):
    convidado = Convidado.objects.get(id=convidado_id)
    parentes = convidado.parentes.all()

    return render(request, 'convidado/confirmacao.html', {
        'convidado': convidado,
        'parentes': parentes,
    })


def erro_confirmacao(request):
    return render(request, 'convidado/erro_confirmacao.html')


