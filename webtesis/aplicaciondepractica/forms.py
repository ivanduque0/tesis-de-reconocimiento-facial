from django import forms

class agregartarea(forms.Form):
    #aqui se agregan los campos que se agregaran al formulario
    tarea = forms.CharField()