from django.shortcuts import redirect, render
from .models import contratos, horariospermitidos, interacciones, usuarios
from .forms import clienteform, contratosform, elegircontrato, clienteformhorarios
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
            interaccioness=interaccioness[::-1]
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

    return redirect(f'/editarcontrato/{contrato}')

def editarusuario(request, cedula_id):
    usuario = usuarios.objects.get(cedula=cedula_id)
    datos = horariospermitidos.objects.filter(cedula=cedula_id)
    if request.method == 'POST':
        formclientehorarios = clienteformhorarios(request.POST)
        if formclientehorarios.is_valid():
            formclientehorarios.save()
    else:
        formclientehorarios = clienteformhorarios({'cedula': cedula_id})

    context = {'usuario':usuario, 'datos': datos, 'formclientehorarios':formclientehorarios}
    return render(request, 'postgrescrud/editarusuario.html', context)

def eliminarhorario(request, id_web):
    horario = horariospermitidos.objects.get(id=id_web)
    cedula_id = horario.cedula.cedula
    horario.delete()

    return redirect(f'/editarusuario/{cedula_id}')


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

