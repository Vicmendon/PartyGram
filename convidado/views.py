from django.shortcuts import render, get_object_or_404
from evento.models import Festa
from .models import Convidado, Parente
from .forms import BuscaConvidadoForm, ConfirmaConvidadoForm
import requests
from datetime import datetime


# FUNÇÃO QUE ENVIA MENSAGEM EM CASO DE ERRO DE CONFIRMAÇÃO DO CONVIDADO
# EXEMPLO O CONVIDADO ESCREVER O NOME DIFERENTE DO QUE TÁ SALVO
# O APP ENVIA MSG PARA O DONO DO EVENTO COM OS DADOS INSERIDOS
def log_erro_whatsapp(nome, whatsapp):
    webhook = 'https://n8nwebhook.star.dev.br/webhook/envia_erro_convidado'
    # webhook = 'https://n8n.star.dev.br/webhook-test/envia_erro_convidado' # teste

    horario = datetime.now()

    r = requests.post(webhook, {
        'hora': horario,
        'convidado': nome,
        'whatsapp': whatsapp
    })

    if r.status_code == 200:
        # db.update_transaction(id_transaction, 'status', 'ENVIADO')
        print(f'Mensagem whatsapp enviada.')
        # time.sleep(random.randint(3, 10))
    else:
        print('STATUS:', r.status_code)
        # time.sleep(random.randint(3, 10))
        hora = datetime.now()
        with open(file='LOG_erros.txt', mode='a', encoding='utf-8') as file:
            file.write(f'\n\n========== {hora} ==========\n{r.text}\n\n{nome} - {whatsapp} - {horario}')


def confirma_presenca(request, hash_evento):
    evento = get_object_or_404(Festa, hash_evento=hash_evento)
    convidados = evento.convidados.all()
    mensagem = None

    if request.method == "POST" and "buscar" in request.POST:
        busca_form = BuscaConvidadoForm(request.POST)
        if busca_form.is_valid():
            telefone = busca_form.cleaned_data['telefone']
            nome = busca_form.cleaned_data['nome']
            print(nome, telefone, evento)
            try:
                convidado = Convidado.objects.get(evento=evento, telefone=telefone, nome=nome)
                print('CONVIDADO:', convidado)
                parentes = convidado.parentes.all()
                print(parentes)
                return render(request, 'convidado/confirmacao.html', {
                    'evento': evento,
                    # 'convidados': convidados,
                    'convidado': convidado,
                    'busca_form': busca_form,
                    'confirma_form': ConfirmaConvidadoForm(instance=convidado),
                    'confirmado': 'Sim',
                    'parentes': parentes
                })
            except Convidado.DoesNotExist:
                log_erro_whatsapp(nome, telefone)
                mensagem = "Convidado não encontrado."
    elif request.method == "POST" and "confirmar" in request.POST:

        infos = request.POST
        print(infos)
        lista_parentes = []
        for info in infos:
            if 'rsvp' in info:
                print(info, request.POST[info])
                if 'convidado_rsvp_' in info:
                    convidado_id = info.replace('convidado_rsvp_', '')
                    print(convidado_id)
                elif 'parente_rsvp_' in info:
                    lista_parentes.append(info)

        # CONFIRMA CONVIDADO
        convidado = get_object_or_404(Convidado, id=convidado_id)
        convidado.rsvp = True
        convidado.save()

        #  CONFIRMA PARENTES
        for parente in lista_parentes:
            parente_id = parente.replace('parente_rsvp_', '')
            parente = get_object_or_404(Parente, id=parente_id)
            parente.rsvp = True
            parente.save()

        # confirma_form = ConfirmaConvidadoForm(request.POST, instance=convidado)
        # if confirma_form.is_valid():
        #     confirma_form.save()
        #     mensagem = "Confirmação registrada com sucesso!"
        mensagem = "Confirmação registrada com sucesso!"

    return render(request, 'convidado/confirmacao.html', {
        'evento': evento,
        'convidados': convidados,
        'busca_form': BuscaConvidadoForm(),
        'mensagem': mensagem
    })
