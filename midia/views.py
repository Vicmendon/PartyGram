from django.shortcuts import render, get_object_or_404, redirect
from .models import Upload, Foto, Video
from evento.models import Festa
from evento.views import visualizar_galeria


def upload_arquivos(request, hash_evento):
    evento = get_object_or_404(Festa, hash_evento=hash_evento)

    if request.method == "POST":

        upload = Upload.objects.create(
            evento=evento,
            usuario=request.user if request.user.is_authenticated else None,
            nome=request.POST.get("nome", ""),
            instagram=request.POST.get("instagram", ""),
            descricao=request.POST.get("descricao", ""),
            privado=request.POST.get("privado", "false") == "true"
        )

        # Salvando as fotos
        for foto in request.FILES.getlist("fotos"):
            Foto.objects.create(upload=upload, imagem=foto)

        # Salvando os vídeos
        for video in request.FILES.getlist("videos"):
            Video.objects.create(upload=upload, video=video)
        
        mensagem = "Arquivos carregados com sucesso!"

        return redirect(visualizar_galeria, evento.hash_evento)

    mensagem = ""
    print('evento:', evento)

    return render(request, "midia/upload.html", {"evento": evento,
                                                 "mensagem": mensagem})

