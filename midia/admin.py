from django.contrib import admin
from .models import Upload, Foto, Video


# Register your models here.
class FotoInline(admin.TabularInline):
    model = Foto
    extra = 0
    fields = ('id', 'imagem', 'visible')
    fk_name = 'upload'


class VideoInline(admin.TabularInline):
    model = Video
    extra = 0
    fields = ('id', 'video', 'visible')
    fk_name = 'upload'


class UploadAdmin(admin.ModelAdmin):
    list_display = ('evento', 'usuario', 'nome', 'data_hora', 'descricao', 'privado')
    search_fields = ('evento', 'nome')
    #list_filter = ('evento', 'rsvp')
    #list_editable = ('rsvp',)
    inlines = [FotoInline, VideoInline]


admin.site.register(Upload, UploadAdmin)
