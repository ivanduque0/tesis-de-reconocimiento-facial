from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.http import HttpResponse
from .models import contratos, fotos, horariospermitidos, interacciones, usuarios
from .forms import clienteform, contratosform, elegircontrato, clienteformhorarios, filtrarinteracciones, filtrarusuarios, subirfoto
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import contratosserializer, usuariosserializer, horariosserializer, interaccionesserializer, fotosserializer
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



# def seleccionarcontratoapi(request):
#     contratoss = contratos.objects.all()
#     if request.method == 'GET':
#         contratos_serializer = contratosserializer(contratoss, many=True)
#         return JsonResponse(contratos_serializer.data, safe=False)

# def editarcontratoapi(request, contrato_id):
#     usuarioss = usuarios.objects.filter(contrato=contrato_id)
#     if request.method == 'GET':
#         usuarios_serializer = usuariosserializer(usuarioss, many=True)
#         return JsonResponse(usuarios_serializer.data, safe=False)
       

# class ContratosList(viewsets.ModelViewSet):
#     queryset = contratos.objects.all()
#     serializer_class = contratosserializer

@csrf_exempt
def agregarcontratosapi(request):
    
    if request.method == 'GET': 
        contratoss = contratos.objects.all()
        contratos_serializer = contratosserializer(contratoss, many=True)
        return JsonResponse(contratos_serializer.data, safe=False)

    elif request.method == 'POST':

        contrato_data = JSONParser().parse(request)
        contrato_serializer = contratosserializer(data=contrato_data)
        if contrato_serializer.is_valid():
            contrato_serializer.save()
            return JsonResponse(contrato_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(contrato_serializer.error, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def eliminarcontratos(request, contrato_id):
    #contrato_id = contrato_id.replace("%20", " ")
    if request.method == 'DELETE':
        contrato=contratos.objects.get(nombre=contrato_id)
        contrato.delete() 
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def seleccionarcontratoapi(request, contrato_id):
    if request.method == 'POST':
        usuarioscontrato = usuarios.objects.filter(contrato=contrato_id)
        usuarioscontrato_serializer = usuariosserializer(usuarioscontrato, many=True)
        return JsonResponse(usuarioscontrato_serializer.data, safe=False)
        # contratoseleccionado_data = JSONParser().parse(request)
        # contratoselecserializer = stringserializer(contratoseleccionado_data)
        #contratoselecserializer.data
        # if contrato_serializer.is_valid():
            #return JsonResponse(contrato_serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
def agregarusuarioapi(request):
    if request.method == 'POST':
        usuario_data = JSONParser().parse(request)
        usuario_serializer = usuariosserializer(data=usuario_data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return JsonResponse(usuario_serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
def eliminarusuarioapi(request, cedula_id):
    if request.method == 'DELETE':
        usuario=usuarios.objects.get(cedula=cedula_id)
        usuario.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def buscarusuarioapi(request, cedula_id):
    if request.method == 'GET':
        usuarioss=usuarios.objects.filter(cedula__icontains=cedula_id)
        usuarioss_serializer = usuariosserializer(usuarioss, many=True)
        # if len(usuarioss) == 1:
        #     usuarioss=usuarioss[0]
        #     usuarioss_serializer = usuariosserializer(usuarioss, many=True)
        return JsonResponse(usuarioss_serializer.data, safe=False)

@csrf_exempt
def editarhorariosapi(request, cedula_id):
    if request.method == 'GET':
        horarios = horariospermitidos.objects.filter(cedula=cedula_id)
        horarios_serializer = horariosserializer(horarios, many=True)
        return JsonResponse(horarios_serializer.data, safe=False)

    if request.method == 'POST':
        horarios_data = JSONParser().parse(request)
        horarios_serializerr = horariosserializer(data=horarios_data)
        if horarios_serializerr.is_valid():
            horarios_serializerr.save()
            return JsonResponse(horarios_serializerr.data, status=status.HTTP_201_CREATED)
        return JsonResponse(horarios_serializer.error, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        horario=horariospermitidos.objects.get(id=cedula_id)
        horario.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def editarfotosapi(request, cedula_id):
    if request.method == 'GET':
        foto = fotos.objects.get(cedula__cedula__icontains=cedula_id)
        foto_serializer = fotosserializer(foto, many=True)
        
        return JsonResponse(foto_serializer.data, safe=False)

    if request.method == 'POST':
        foto_data = JSONParser().parse(request)
        foto_serializer = horariosserializer(data=foto)
        if foto_serializer.is_valid():
            foto_serializer.save()
            return JsonResponse(foto_serializer.data, status=status.HTTP_201_CREATED)
    