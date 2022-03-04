from django import forms
from .models import oficina

class clienteform(forms.ModelForm):

    class Meta:
        model = oficina
        fields = ['cedula', 'nombre']