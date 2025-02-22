from django.shortcuts import render, get_object_or_404, redirect
from .models import Upload, Foto, Video
from evento.models import Festa
from evento.views import visualizar_galeria
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


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

        #return render(request, "evento/gallery.html", hash_evento=hash_evento)
        #return redirect(reverse('galeria', kwargs={'hash_evento': evento.hash_evento}))
        #return redirect(visualizar_galeria, evento.hash_evento)
        # TENTEI FAZER UM REDIRECT PRA GALERIA DEPOIS DO UPLOAD, MAS NÃO ROLOU.

        return render(request, "midia/upload.html", {"evento": evento,
                                                 "mensagem": mensagem})

    print('evento:', evento)

    return render(request, "midia/upload.html", {"evento": evento})


@staff_member_required
@csrf_exempt  # Se necessário, dependendo da configuração do CSRF
def remove_media(request, hash_evento, media_type, media_id):
    if request.method == 'DELETE':
        try:
            if media_type == 'foto':
                media = Foto.objects.get(id=media_id)
            elif media_type == 'video':
                media = Video.objects.get(id=media_id)
            else:
                return JsonResponse({'error': 'Tipo de mídia inválido'}, status=400)
            
            #media.delete()
            media.visible = False
            media.save()
            return JsonResponse({'success': 'Mídia removida com sucesso'}, status=200)
        except (Foto.DoesNotExist, Video.DoesNotExist):
            return JsonResponse({'error': 'Mídia não encontrada'}, status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])