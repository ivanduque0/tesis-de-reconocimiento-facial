from django.shortcuts import render, redirect
from .forms import agregartarea

tareas=["practicar con django", "aprender a usar bases de datos con django", "aprender a usar angular", "intentar mejorar el modelo de reconocmiento facial optimizandolo"]

def home(request):
    context = {'tareas':tareas}
    return render(request,"aplicaciondepractica/home.html",context)

def agregar(request):
    #asi se configuran las request en django
    #esto se hace cuando el servidor recibe un post proveniente del cliente
    if request.method == 'POST':
        #aqui se mira lo que se envio en el input
        form = agregartarea(request.POST)
        if form.is_valid():
            #el nombre de "tarea" debe ser el mismo que el usado en el input en el archivo forms.py
            tarea = form.cleaned_data["tarea"]
            #aqui se agrega lo que se recibio en el input a la lista de tareas
            tareas.append(tarea)
            #asi se hace que al completar algo se redireccione
            #automaticamente al link que se desee
            return redirect('home')
    else:
        #esto es lo que se va a mostrar cuando el servidor reciba un GET proveniente del cliente
        form=agregartarea()
    context = {'form':form}
    return render(request, "aplicaciondepractica/agregartarea.html",context)

