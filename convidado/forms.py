from django import forms
from .models import Convidado, Parente


class BuscaConvidadoForm(forms.Form):
    nome = forms.CharField(max_length=50, label="Primeiro Nome", required=True)
    telefone = forms.CharField(max_length=16, label="Whatsapp", required=True)


class ConfirmaConvidadoForm(forms.ModelForm):
    class Meta:
        model = Convidado
        fields = ['rsvp']


class ConfirmaParenteForm(forms.ModelForm):
    class Meta:
        model = Parente
        fields = ['rsvp']
