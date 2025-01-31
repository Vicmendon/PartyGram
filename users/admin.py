from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Campos a serem exibidos no Django Admin
    list_display = ("email", "nome", "sobrenome", "telefone", "is_staff", "is_active")
    search_fields = ("email", "nome", "sobrenome", "telefone")
    ordering = ("email",)

    # Campos editáveis na interface do Django Admin
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações Pessoais", {"fields": ("nome", "sobrenome", "telefone")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Campos para adicionar usuários manualmente no Admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nome", "sobrenome", "telefone", "password1", "password2", "is_staff", "is_active"),
        }),
    )

admin.site.register(User, CustomUserAdmin)

