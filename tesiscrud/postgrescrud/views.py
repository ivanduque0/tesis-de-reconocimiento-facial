from django.shortcuts import redirect, render
from .models import contratos, interacciones, usuarios
from .forms import clienteform, contratosform, elegircontrato
# Create your views here.

def interaccionesss(request):
    interaccioness = []
    usuarioss = []
    contratoo=''
    if request.method == "POST":
        select=elegircontrato(request.POST)
        if select.is_valid():
            contratoo=select.cleaned_data.get('contrato')
            contratoinstancia = contratos.objects.get(nombre=contratoo)
            usuarioss = contratoinstancia.contrato.all()
            interaccioness = interacciones.objects.filter(contrato=contratoo)
    else:
        select=elegircontrato()
    

    context= {'interaccioness': interaccioness, 'usuarios':usuarioss, 'contratos':contratoo,'select':select}
    return render(request, 'postgrescrud/interacciones.html',context)

def index(request):
    return render(request, 'postgrescrud/index.html')

def editarcontrato(request, contrato_id):
    #contratoss = contratos.objects.all()
    select=elegircontrato()
    usuarioss = usuarios.objects.filter(contrato=contrato_id)
    if request.method == 'POST':
        formcliente = clienteform(request.POST)
        if formcliente.is_valid():
            formcliente.save()
    else:
        formcliente = clienteform({'contrato': contrato_id})
    
    clienteform 
    context = {'formcliente' : formcliente, 'usuarios':usuarioss, 'contrato':contrato_id, 'select':select} #'usuarios':usuarioss,

    return render(request, 'postgrescrud/editarcontrato.html', context)

def eliminarusuario(request, cedula_id):
    usuario = usuarios.objects.get(cedula=cedula_id)
    contrato = usuario.contrato
    usuario.delete()

    return redirect(f'/editarcontrato/{contrato}/')

def agregarcontrato(request):
    contratoss = contratos.objects.all()
    if request.method == 'POST':
        formcontrato = contratosform(request.POST)
        if formcontrato.is_valid():
            formcontrato.save()
    else:
        formcontrato = contratosform()
    
    context = {'formcontrato' : formcontrato, 'contratos': contratoss}

    return render(request, 'postgrescrud/agregarcontrato.html', context)


def eliminarcontrato(request, contrato_id):
    contrato = contratos.objects.get(nombre=contrato_id)
    contrato.delete()

    return redirect('agregarcontrato')

def seleccionarcontrato(request):
    if request.method == "POST":
        select=elegircontrato(request.POST)
        if select.is_valid():
            contratoo=select.cleaned_data.get('contrato')
    else:
        select=elegircontrato()
        contratoo=0
    #cont= request.GET['contrato']
    #'usuarios':usuarioss,
    usuarioss = usuarios.objects.filter(contrato=contratoo)
    cantidadusuarios = len(usuarioss)
    context = {'select':select, 'contrato':contratoo, 'usuarios':usuarioss, 'cantidad':cantidadusuarios}
    return render(request, 'postgrescrud/seleccionarcontrato.html', context)

