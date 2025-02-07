from django.db import models
from users.models import User
from evento.models import Festa

from PIL import Image
import os
import cv2
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO


class Upload(models.Model):
    evento = models.ForeignKey(Festa, on_delete=models.SET_NULL, related_name="uploads", null=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # Se logado
    nome = models.CharField(max_length=255, blank=True, null=True)  # Caso seja sem login
    instagram = models.CharField(max_length=100, blank=True, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True, null=True)
    privado = models.BooleanField(default=False)  # True = só quem enviou e donos do evento veem

    def __str__(self):
        return f"Upload por {self.usuario if self.usuario else self.nome} no evento {self.evento}"


# Função para definir o caminho do upload dinamicamente
def caminho_upload_fotos(instance, filename):
    nome_evento = instance.upload.evento.nome.replace(" ", "_")
    return os.path.join(nome_evento, "uploads", "fotos", filename)


def caminho_upload_videos(instance, filename):
    nome_evento = instance.upload.evento.nome.replace(" ", "_")
    return os.path.join(nome_evento, "uploads", "videos", filename)


def caminho_upload_fotos_thumbnails(instance, filename):
    nome_evento = instance.upload.evento.nome.replace(" ", "_")
    return os.path.join(nome_evento, "uploads", "fotos", "thumbnails", filename)

def caminho_upload_videos_thumbnails(instance, filename):
    nome_evento = instance.upload.evento.nome.replace(" ", "_")
    return os.path.join(nome_evento, "uploads", "videos", "thumbnails", filename)


class Foto(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name="fotos")  # Permite várias fotos
    imagem = models.ImageField(upload_to=caminho_upload_fotos)
    miniatura = models.ImageField(upload_to=caminho_upload_fotos_thumbnails, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    #curtidas = models.ManyToOneRel(User, related_name="user", )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagem and not self.miniatura:
            self.gerar_miniatura()
    
    def gerar_miniatura(self):
        img = Image.open(self.imagem.path)
        img.thumbnail((200, 200))  # Reduz a imagem para miniatura
        thumb_filename = f"thumb_{os.path.basename(self.imagem.path)}"
        thumb_path = os.path.join(os.path.dirname(self.imagem.path), "thumbnails", thumb_filename)

        if not os.path.exists(os.path.dirname(thumb_path)):
            os.makedirs(os.path.dirname(thumb_path))  # Cria a pasta de miniaturas se não existir

        img.save(thumb_path)
        self.miniatura = os.path.join(self.upload.evento.nome.replace(" ", "_"), "uploads", "fotos", "thumbnails", thumb_filename)
        super().save(update_fields=["miniatura"])
    
    def __str__(self):
        return f"Foto de {self.upload}"
    
    def get_thumbnail(self):
        return self.miniatura.url if self.miniatura else "/static/midia/sem_thumb.jpg"
    
    def get_url(self):
        return self.imagem.url if self.imagem else "/static/midia/sem_thumb.jpg"


class Video(models.Model):
    upload = models.ForeignKey("Upload", on_delete=models.CASCADE, related_name="videos")  
    video = models.FileField(upload_to=caminho_upload_videos, max_length=300)
    thumbnail = models.ImageField(upload_to=caminho_upload_videos_thumbnails, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    #curtidas = models.ManyToOneRel(User, related_name="user", )


    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url  # Retorna a imagem do upload
        return "/static/midia/sem_thumb.jpg"  # Retorna a imagem padrão

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.video and not self.thumbnail:
            self.gerar_thumbnail()

    def gerar_thumbnail(self):
        video_path = self.video.path
        nome_evento = self.upload.evento.nome.replace(" ", "_")
        thumb_dir = os.path.join(os.path.dirname(video_path), "thumbnails")

        # 🔹 Garante que a pasta existe antes de salvar
        os.makedirs(thumb_dir, exist_ok=True)

        thumb_filename = f"thumb_{os.path.splitext(os.path.basename(video_path))[0]}.jpg"
        thumb_path = os.path.join(thumb_dir, thumb_filename)

        # 🔹 Tenta capturar um frame do vídeo
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Erro ao abrir o vídeo: {video_path}")
            return

        cap.set(cv2.CAP_PROP_POS_FRAMES, 10)  # Captura um frame nos primeiros segundos
        ret, frame = cap.read()
        cap.release()

        if not ret:
            print(f"Não foi possível capturar um frame do vídeo: {video_path}")
            return

        # 🔹 Salva o frame como imagem
        sucesso = cv2.imwrite(thumb_path, frame)

        if not sucesso:
            print(f"Erro ao salvar a miniatura: {thumb_path}")
            return

        # 🔹 Confirma se o arquivo realmente existe antes de tentar abrir
        if os.path.exists(thumb_path):
            with open(thumb_path, "rb") as f:
                self.thumbnail.save(thumb_filename, ContentFile(f.read()), save=True)
        else:
            print(f"Miniatura não foi encontrada após a tentativa de salvar: {thumb_path}")

    def get_url(self):
        return self.video.url if self.video else "/static/midia/sem_thumb.jpg"

    def __str__(self):
        return f"Vídeo de {self.upload}"
    

class Comentarios(models.Model):
    CHOICES_POSTAGEM = [
        ('IMG', 'Imagem'),
        ('VID', 'Vídeo')
    ]
    
    tipo_postagem = models.CharField(max_length=3, choices=CHOICES_POSTAGEM)
    id_imagem = models.ForeignKey(Foto, on_delete=models.CASCADE, null=True, blank=True)
    id_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    comentario = models.TextField(max_length=500)
    #curtidas = models.ManyToOneRel(User, related_name="user")