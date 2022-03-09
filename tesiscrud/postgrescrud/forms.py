from select import select
from attr import fields
from django import forms
from .models import contratos, usuarios, horariospermitidos

class clienteform(forms.ModelForm):

    class Meta:
        model = usuarios
        fields = ['cedula', 'nombre', 'contrato']

class clienteformhorarios(forms.ModelForm):

    class Meta:
        model = horariospermitidos
        fields = ['cedula', 'dia', 'entrada', 'salida']

class contratosform(forms.ModelForm):

    class Meta:
        model= contratos
        fields = ['nombre']

class elegircontrato(forms.Form):
    contrato=forms.ModelChoiceField(queryset=contratos.objects.all(), widget=forms.Select)
