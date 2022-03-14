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

class filtrarinteracciones(forms.Form):
    #cedula=forms.ModelChoiceField(queryset=usuarios.objects.values_list('cedula', flat=True).distinct(), widget=forms.Select, required=False)
    cedula=forms.IntegerField(required=False)
    fechadesde=forms.DateField(required=False) #aaaa-mm-dd
    fechahasta=forms.DateField(required=False) #aaaa-mm-dd
    horadesde=forms.TimeField(required=False) #hh:mm
    horahasta=forms.TimeField(required=False) #hh:mm

class filtrarusuarios(forms.Form):
    cedulaf=forms.IntegerField(required=False, label="Buscar por cedula")