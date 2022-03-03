from django import forms
from .models import oficina

class clienteform(forms.ModelForm):

    class datos:
        model: oficina
        fields = ['cedula', 'nombre']