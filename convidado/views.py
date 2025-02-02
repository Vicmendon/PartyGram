from django.shortcuts import render, get_object_or_404
from evento.models import Festa
from .models import Convidado, Parente
from .forms import BuscaConvidadoForm, ConfirmaConvidadoForm
import requests
from datetime import datetime

# imports para msg assíncrona do whatsapp
import threading
import time
import queue    # usar no próximo upgrade


def send_message_async(whatsapp='', mensagem='', nome=''):

    if nome != '' and whatsapp != '':
        try:
            thread = threading.Thread(target=log_erro_whatsapp, args=(nome, whatsapp))
            thread.start()
        except Exception as e:
            print(e)
    
    elif mensagem != '':
        try:
            thread = threading.Thread(target=msg_convidado_confirmado, args=(mensagem,))
            thread.start()
        except Exception as e:
            print(e)


def log_erro_whatsapp(nome, whatsapp):
    webhook = 'https://n8nwebhook.star.dev.br/webhook/envia_erro_convidado'

    time.sleep(5)

    horario = datetime.now()
    
    try:
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
    except Exception as e:
        hora = datetime.now()
        with open(file='LOG_erros.txt', mode='a', encoding='utf-8') as file:
            file.write(f'\n\n========== {hora} ==========\n{r.text}\n\n{nome} - {whatsapp} - {horario}\n\n{e}')


def msg_convidado_confirmado(mensagem):
    webhook = 'https://n8nwebhook.star.dev.br/webhook/envia_confirmacao'

    time.sleep(5)

    horario = datetime.now()

    try:
        r = requests.post(webhook, {
            'hora': horario,
            'mensagem': mensagem
        })

        if r.status_code == 200:
            # db.update_transaction(id_transaction, 'status', 'ENVIADO')
            print(f'Mensagem confirmação enviada.')
            # time.sleep(random.randint(3, 10))
        else:
            print('STATUS:', r.status_code)
            # time.sleep(random.randint(3, 10))
            hora = datetime.now()
            with open(file='LOG_erros_confirmação.txt', mode='a', encoding='utf-8') as file:
                file.write(f'\n\n========== {hora} ==========\n{r.text}\n\n{mensagem} - {horario}')
    except Exception as e:
        hora = datetime.now()
        with open(file='LOG_erros_confirmação.txt', mode='a', encoding='utf-8') as file:
            file.write(f'\n\n========== {hora} ==========\n{r.text}\n\n{mensagem} - {horario}\n\n{e}')


def confirma_presenca(request, hash_evento):
    evento = get_object_or_404(Festa, hash_evento=hash_evento)
    convidados = evento.convidados.all()
    mensagem = None

    if request.method == "POST" and "buscar" in request.POST:
        busca_form = BuscaConvidadoForm(request.POST)
        if busca_form.is_valid():
            #print('REQUEST POST PESQUISA:', request.POST)
            telefone = busca_form.cleaned_data['telefone']
            nome = busca_form.cleaned_data['nome']
            #print(nome, telefone, evento)
            try:
                convidado = Convidado.objects.get(evento=evento, telefone=telefone)

                # tratamento do nome para evitar erros do usuário
                # REFAZ NOMES SEM ACENTUAÇÃO
                nome_novo = ''
                nome_db_novo = ''
                for letra in nome:
                    if letra.lower() in ['á', 'à', 'ã', 'â']:
                        letra = 'a'
                    elif letra.lower() in ['é', 'è', 'ê']:
                        letra = 'e'
                    elif letra.lower() in ['í', 'ì', 'î']:
                        letra = 'i'
                    elif letra.lower() in ['õ', 'ó', 'ò', 'ô']:
                        letra = 'o'
                    elif letra.lower() in ['ú', 'ù', 'û']:
                        letra = 'u'
                    elif letra.lower() in ['ç']:
                        letra = 'c'
                    
                    nome_novo += letra
                
                for letra in convidado.nome:
                    if letra.lower() in ['á', 'à', 'ã', 'â']:
                        letra = 'a'
                    elif letra.lower() in ['é', 'è', 'ê']:
                        letra = 'e'
                    elif letra.lower() in ['í', 'ì', 'î']:
                        letra = 'i'
                    elif letra.lower() in ['õ', 'ó', 'ò', 'ô']:
                        letra = 'o'
                    elif letra.lower() in ['ú', 'ù', 'û']:
                        letra = 'u'
                    elif letra.lower() in ['ç']:
                        letra = 'c'
                    
                    nome_db_novo += letra

                nomes_possiveis = nome_novo.split(' ')
                for nomee in nomes_possiveis:
                    nomee = nomee.lower()

                if nome_db_novo.lower() in nomes_possiveis:
                    #print('CONVIDADO:', convidado)
                    parentes = convidado.parentes.all()
                    #print(parentes)
                    for parente in parentes:
                        print(parente.rsvp, parente.id)
                    return render(request, 'convidado/confirmacao.html', {
                        'evento': evento,
                        # 'convidados': convidados,
                        'convidado': convidado,
                        'busca_form': busca_form,
                        'confirma_form': ConfirmaConvidadoForm(instance=convidado),
                        'confirmado': 'Sim',
                        'parentes': parentes})
                else:
                    send_message_async(telefone, '', nome)
                    mensagem = "Convidado não encontrado." 
            except Convidado.DoesNotExist:
                send_message_async(telefone, '', nome)
                mensagem = "Convidado não encontrado."
    elif request.method == "POST" and "confirmar" in request.POST:
        infos = request.POST
        # print('INFOS', infos)
        lista_parentes = []
        for info in infos:
            # print('INFO:', info, request.POST[info])
            if 'convidado' in info or 'parente' in info:
                # print(info, request.POST[info])
                if 'convidado-' in request.POST[info]:
                    convidado_id = request.POST[info].split('-')[1]
                    convidado_rsvp = request.POST[info].split('-')[2]
                    # print('ID CONVIDADO:', convidado_id, convidado_rsvp)
                elif 'parente-' in request.POST[info]:
                    # print('PARENTE LOCALIZADO:', info.replace('parente-', ''))
                    lista_parentes.append({
                        'id': request.POST[info].split('-')[1],
                        'rsvp': request.POST[info].split('-')[2]
                    })

        # CONFIRMA CONVIDADO
        convidado = get_object_or_404(Convidado, id=convidado_id)
        # print(f'CONVIDADO -> {convidado}')
        convidado.rsvp = convidado_rsvp
        convidado.save()

        # MANDA WHATSAPP DE CONFIRMAÇÃO
        if convidado_rsvp == 'SIM':
            msg_confirmacao = f'Convidado {convidado.nome} {convidado.sobrenome} confirmado! Whatsapp: {convidado.telefone}'
        elif convidado_rsvp == 'NÃO':
            msg_confirmacao = f'Convidado {convidado.nome} {convidado.sobrenome} recusou! Whatsapp: {convidado.telefone}'

        send_message_async('', msg_confirmacao, '')

        #  CONFIRMA PARENTES
        for parente in lista_parentes:
            #parente_id = parente.replace('parente_rsvp_', '')
            parente_db = get_object_or_404(Parente, id=parente['id'])
            parente_db.rsvp = parente['rsvp']
            parente_db.save()

            if parente['rsvp'] == 'SIM':
                msg_confirmacao = f'Convidado {convidado.nome} {convidado.sobrenome} *confirmou* a presença de {parente_db.nome}! Whatsapp: {convidado.telefone}'
            elif parente['rsvp'] == 'NÃO':
                msg_confirmacao = f'Convidado {convidado.nome} {convidado.sobrenome} *recusou* a presença de {parente_db.nome}! Whatsapp: {convidado.telefone}'

            send_message_async('', msg_confirmacao, '')

        mensagem = "Confirmação registrada com sucesso!"

    return render(request, 'convidado/confirmacao.html', {
        'evento': evento,
        'convidados': convidados,
        'busca_form': BuscaConvidadoForm(),
        'mensagem': mensagem
    })
