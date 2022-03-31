from django.shortcuts import redirect, render
from .models import contratos, fotos, horariospermitidos, interacciones, usuarios
from .forms import clienteform, contratosform, elegircontrato, clienteformhorarios, filtrarinteracciones, filtrarusuarios, subirfoto
import os
# Create your views here.
directorio = '/home/ivan/Desktop/appdocker'
def interaccionesss(request):
    interaccioness = []
    interaccionesss= []
    usuarioss = []
    contratoo= None
    cedulafiltro=None
    fechadesdefiltro=None
    fechahastafiltro=None
    horadesdefiltro=None
    horahastafiltro=None
    cantidadusuarios=0
    cantidadinteracciones=0

    if request.method == "POST":
        select=elegircontrato(request.POST)
        filtro=filtrarinteracciones(request.POST)
        
        if select.is_valid():
            contratoo=select.cleaned_data.get('contrato')
            contratoinstancia = contratos.objects.get(nombre=contratoo)
            usuarioss = contratoinstancia.contrato.all()
        
        if filtro.is_valid():
            cedulafiltro=filtro.cleaned_data.get('cedula')
            fechadesdefiltro=filtro.cleaned_data.get('fechadesde')
            fechahastafiltro=filtro.cleaned_data.get('fechahasta')
            horadesdefiltro=filtro.cleaned_data.get('horadesde')
            horahastafiltro=filtro.cleaned_data.get('horahasta')
            select=elegircontrato({'contrato': contratoo})
            
        if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo)
            

        if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__gte=fechadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__lte=fechahastafiltro)
            

        if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__lte=fechahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro)
            

        if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro)
            

        if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__gte=fechadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro)
            

        if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro)
            

        if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)
            

        if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)
            

        if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
            interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)
            
        interaccionesss = interaccioness[::-1]
        if cedulafiltro == None and (fechadesdefiltro != None or fechahastafiltro != None or horadesdefiltro != None or horahastafiltro != None):
            #nombreslista = interaccioness.values_list('nombre', flat=True)
            cedulaslista = interaccioness.values_list('cedula', flat=True)
            cedulasunicaslista=[]
            usuarioss=[]
            for cedula in cedulaslista:
                if not cedula in cedulasunicaslista:
                    cedulasunicaslista.append(cedula)
            for cedulaunica in cedulasunicaslista:
                usuarioss.append(usuarios.objects.get(cedula=cedulaunica))

        if cedulafiltro != None and len(interaccioness)>0:
            cedulaslista = interaccioness.values_list('cedula', flat=True)
            cedulasunicaslista=[]
            usuarioss=[]
            for cedula in cedulaslista:
                if not cedula in cedulasunicaslista:
                    cedulasunicaslista.append(cedula)
            for cedulaunica in cedulasunicaslista:
                usuarioss.append(usuarios.objects.get(cedula=cedulaunica))
        if cedulafiltro != None and len(interaccioness)==0:
            usuarioss = []
        cantidadinteracciones=len(interaccioness)
        cantidadusuarios=len(usuarioss)

    else:
        select=elegircontrato()
        filtro=filtrarinteracciones()

    context= {'interaccioness': interaccionesss, 'usuarios':usuarioss, 'contratos':contratoo,'select':select,'filtro':filtro,'cedulafiltro':cedulafiltro,'fechadesdefiltro':fechadesdefiltro,'fechahastafiltro':fechahastafiltro,'horadesdefiltro':horadesdefiltro,'horahastafiltro':horahastafiltro, 'cantidadinteracciones':cantidadinteracciones, 'cantidadusuarios':cantidadusuarios}
    return render(request, 'web/interacciones.html',context)

def index(request):
    return render(request, 'web/index.html')

def editarcontrato(request, contrato_id):
    #contratoss = contratos.objects.all()
    cedulafiltro=None
    usuarioss = usuarios.objects.filter(contrato=contrato_id)
    cant1 = len(usuarioss)
    select=elegircontrato({'contrato': contrato_id})
    if request.method == 'POST':
        formcliente = clienteform(request.POST)
        filtro= filtrarusuarios(request.POST)
        if filtro.is_valid():
            cedulafiltro=filtro.cleaned_data.get('cedulaf')
            if cedulafiltro!=None:
                usuarioss = usuarios.objects.filter(cedula__contains=cedulafiltro)
        if formcliente.is_valid():
            formcliente.save()

    else:
        formcliente = clienteform({'contrato': contrato_id})
        filtro = filtrarusuarios()
        usuarioss = usuarios.objects.filter(contrato=contrato_id)

    if cedulafiltro==None:
        usuarioss = usuarios.objects.filter(contrato=contrato_id)

    cantidadusuarios = len(usuarioss)
    context = {'formcliente' : formcliente, 'usuarios':usuarioss, 'contrato':contrato_id,'select':select, 'filtro':filtro, 'cantidad':cantidadusuarios, 'cedulafiltro':cedulafiltro} #'usuarios':usuarioss,


    if len(usuarios.objects.filter(contrato=contrato_id)) != cant1 and cedulafiltro==None:
        return redirect(f'/editarcontrato/{contrato_id}')

    return render(request, 'web/editarcontrato.html', context)

def eliminarusuario(request, cedula_id):
    usuario = usuarios.objects.get(cedula=cedula_id)
    contrato = usuario.contrato
    usuario.delete()

    return redirect(f'/editarcontrato/{contrato}')

def editarusuario(request, cedula_id):
    usuario = usuarios.objects.get(cedula=cedula_id)
    datos = horariospermitidos.objects.filter(cedula=cedula_id)
    foto = fotos.objects.filter(cedula__cedula__icontains=cedula_id)
    if foto:
        foto = foto[0]
    if request.method == 'POST':
        formclientehorarios = clienteformhorarios(request.POST)
        formfoto = subirfoto(request.POST, request.FILES)
        if formclientehorarios.is_valid():
            formclientehorarios.save()
        if formfoto.is_valid():
            formfoto.save()   
            foto = fotos.objects.filter(cedula__cedula__icontains=cedula_id)
            if foto:
                foto = foto[0]
            #imagen = formfoto.cleaned_data['img']

    else:
        formclientehorarios = clienteformhorarios({'cedula': cedula_id})
        formfoto = subirfoto({'cedula': cedula_id})

    context = {'usuario':usuario, 'datos': datos, 'formclientehorarios':formclientehorarios, 'formfoto':formfoto, 'foto':foto}
    return render(request, 'web/editarusuario.html', context)

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

    return render(request, 'web/agregarcontrato.html', context)

def eliminarcontrato(request, contrato_id):
    contrato = contratos.objects.get(nombre=contrato_id)
    usuarioscontrato = usuarios.objects.filter(contrato=contrato_id)
    foto = None
    for usuariofoto in usuarioscontrato:
        usuariocedula = usuariofoto.cedula
        foto = fotos.objects.filter(cedula__cedula__icontains=usuariocedula)
        if len(foto) > 0:
            foto=foto[0]
            foto.foto.delete(save=False)
    contrato.delete()

    return redirect('agregarcontrato')

def eliminarfoto(request, cedula_id):
    foto = fotos.objects.get(cedula=cedula_id)
    foto.foto.delete(save=False)
    foto.delete()

    return redirect(f'/editarusuario/{cedula_id}')


def seleccionarcontrato(request):
    if request.method == "POST":
        select=elegircontrato(request.POST)
        if select.is_valid():
            contratoo=select.cleaned_data.get('contrato')
    else:
        select=elegircontrato()
        contratoo=None
    #cont= request.GET['contrato']
    #'usuarios':usuarioss,
    usuarioss = usuarios.objects.filter(contrato=contratoo)
    cantidadusuarios = len(usuarioss)
    context = {'select':select, 'contrato':contratoo, 'usuarios':usuarioss, 'cantidad':cantidadusuarios}
    return render(request, 'web/seleccionarcontrato.html', context)

