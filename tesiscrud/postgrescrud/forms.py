from select import select
from attr import fields
from django import forms
from .models import contratos, horariospermitidos, usuarios

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

class filtrarinteracciones(forms.Form):
    nombre=forms.ModelChoiceField(queryset=usuarios.objects.values_list('nombre').distinct(), widget=forms.Select, required=False)
    cedula=forms.ModelChoiceField(queryset=usuarios.objects.values_list('cedula').distinct(), widget=forms.Select, required=False)
    fecha=forms.DateField(required=False)
    horadesde=forms.TimeField(required=False)
    horahasta=forms.TimeField(required=False)
    razon=forms.CharField(required=False)