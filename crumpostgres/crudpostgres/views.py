from django.shortcuts import redirect, render
from .models import interacciones, oficina
from .forms import clienteform
# Create your views here.

def home(request):
    interaccioness = interacciones.objects.all()
    interaccioness = interaccioness[::-1]
    context= {'interaccioness': interaccioness}
    return render(request, 'crudpostgres/home.html',context)

def agregarusuario(request):
    if request.method == 'POST':
        form = clienteform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = clienteform()
    context= {'form' : form}
    return render(request, 'crudpostgres/agregar.html',context)


