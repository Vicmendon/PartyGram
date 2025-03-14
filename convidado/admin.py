from django.contrib import admin
from .models import Convidado, Parente

# Register your models here.


class ParenteInline(admin.TabularInline):
    model = Parente
    extra = 0
    fields = ('nome', 'idade', 'cervejeiro', 'rsvp')
    fk_name = 'convidado'


class ParenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'convidado', 'rsvp')
    list_editable = ('rsvp',)
    # search_fields = ('nome', 'convidado')
    # list_filter = ('evento', 'rsvp')


class ConvidadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'email', 'rsvp', 'evento')
    search_fields = ('nome', 'email')
    #list_filter = ('evento', 'rsvp')
    list_editable = ('rsvp',)
    inlines = [ParenteInline]


admin.site.register(Convidado, ConvidadoAdmin)
admin.site.register(Parente, ParenteAdmin)
