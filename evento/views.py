from django.shortcuts import render, get_object_or_404
from .models import Festa
from midia.models import Upload, Foto, Video


'''
def visualizar_uploads(request, hash_evento):
    evento = get_object_or_404(Festa, hash_evento=hash_evento)
    uploads = Upload.objects.filter(evento=evento)
    
    return render(request, "evento/uploads.html", {"evento": evento, "uploads": uploads})
'''


def visualizar_galeria(request, hash_evento):
    festa = get_object_or_404(Festa, hash_evento=hash_evento)
    
    print('FESTA ENCONTRADA:', festa)

    # Recupera os uploads da festa
    uploads = Upload.objects.filter(evento=festa)
    
    # Filtra fotos e vídeos baseados nos uploads
    fotos = Foto.objects.filter(upload__in=uploads)
    videos = Video.objects.filter(upload__in=uploads)

    for foto in fotos:
        print('FOTO:', foto.imagem)
        print('MINIATURA:', foto.miniatura)
    
    print('--------------------------')
    print(Foto.objects.all())
    print(Video.objects.all())

    midias = list(fotos) + list(videos)

    return render(request, "evento/gallery.html", {"midias": midias, "festa": festa})