from django.contrib import admin
from .models import Festa
from convidado.models import Convidado

# Register your models here.
class FestaAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'data', 'organizador', 'total_convidados_display', 
        'total_confirmados_display', 'total_recusaram_display', 
        'total_cervejeiros_display'
        )
    
    list_filter = ('data', 'organizador')

    def total_convidados_display(self, obj):
        return obj.total_convidados()
    total_convidados_display.short_description = 'Convidados'

    def total_confirmados_display(self, obj):
        return obj.total_confirmados()
    total_confirmados_display.short_description = 'Confirmados'

    
    def total_recusaram_display(self, obj):
        return obj.total_recusaram()
    total_recusaram_display.short_description = 'Não vão'

    def total_cervejeiros_display(self, obj):
        return obj.total_cervejeiros()
    total_cervejeiros_display.short_description = 'Cervejeiros'


admin.site.register(Festa, FestaAdmin)
