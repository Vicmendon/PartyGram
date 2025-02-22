import sqlite3
import django
import os
import random
import string

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainproject.settings')
django.setup()

from evento.models import Festa
from users.models import User
from convidado.models import Convidado, Parente, LogEventos

# Conectar ao banco de backup
backup_conn = sqlite3.connect('db_backup.sqlite3')
backup_cursor = backup_conn.cursor()


# ✅ **1. Importar Eventos (Festa)**
backup_cursor.execute("SELECT id, nome, data, descricao, organizador_id, horas, bairro, cidade, endereco, compl_endereco, estado, GPS FROM evento_festa")
eventos = backup_cursor.fetchall()

for evento in eventos:
    organizador = User.objects.filter(id=evento[4]).first()
    if not organizador:
        print(f"⚠️ ERRO: Organizador ID {evento[4]} não encontrado para evento {evento[1]}. Pulando...")
        continue

    festa, created = Festa.objects.get_or_create(
        id=evento[0],
        defaults={
            "nome": evento[1],
            "data": evento[2],
            "descricao": evento[3],
            "organizador": organizador,
            "horas": evento[5],
            "bairro": evento[6],
            "cidade": evento[7],
            "endereco": evento[8],
            "compl_endereco": evento[9],
            "estado": evento[10],
            "GPS": evento[11],
            "hash_evento": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        }
    )
    print(f"🎉 Evento {'criado' if created else 'já existe'}: {evento[1]}")

# ✅ **2. Importar Convidados**
backup_cursor.execute("SELECT id, telefone, email, nome, sobrenome, rsvp, evento_id FROM convidado_convidado")
convidados = backup_cursor.fetchall()

for convidado in convidados:
    evento = Festa.objects.filter(id=convidado[6]).first()
    if evento:
        convidado_obj, created = Convidado.objects.get_or_create(
            id=convidado[0],
            defaults={
                "telefone": convidado[1],
                "email": convidado[2],
                "nome": convidado[3],
                "sobrenome": convidado[4],
                "rsvp": convidado[5],
                "evento": evento,
            }
        )
        print(f"📩 Convidado {'criado' if created else 'já existe'}: {convidado[3]} {convidado[4]}")
    else:
        print(f"⚠️ ERRO: Evento ID {convidado[6]} não encontrado para convidado {convidado[3]} {convidado[4]}")

# ✅ **3. Importar Parentes**
backup_cursor.execute("SELECT id, nome, rsvp, convidado_id, idade, cervejeiro FROM convidado_parente")
parentes = backup_cursor.fetchall()

for parente in parentes:
    convidado = Convidado.objects.filter(id=parente[3]).first()
    if convidado:
        parente_obj, created = Parente.objects.get_or_create(
            id=parente[0],
            defaults={
                "nome": parente[1],
                "rsvp": parente[2],
                "convidado": convidado,
                "idade": parente[4],
                "cervejeiro": bool(parente[5])
            }
        )
        print(f"👨‍👩‍👦 Parente {'criado' if created else 'já existe'}: {parente[1]}")
    else:
        print(f"⚠️ ERRO: Convidado ID {parente[3]} não encontrado para parente {parente[1]}")

# ✅ **4. Importar Logs de Eventos**
backup_cursor.execute("SELECT id, usuario_id, hora, registro FROM convidado_logeventos")
logs = backup_cursor.fetchall()

for log in logs:
    usuario = Convidado.objects.filter(id=log[1]).first()
    if usuario:
        log_obj, created = LogEventos.objects.get_or_create(
            id=log[0],
            defaults={
                "usuario": usuario,
                "hora": log[2],
                "registro": log[3]
            }
        )
        print(f"📜 Log {'criado' if created else 'já existe'} para {usuario.nome}")
    else:
        print(f"⚠️ ERRO: Convidado ID {log[1]} não encontrado para log {log[3]}")

# 🔥 **Finalizando Importação**
backup_conn.close()
print("\n✅ **Importação concluída com sucesso!** 🚀")
