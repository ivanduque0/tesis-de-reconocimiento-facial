from hashlib import new
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.http import HttpResponse
from .models import contratos, fotos, horariospermitidos, interacciones, usuarios, apertura, dispositivos, User
#from .forms import clienteform, contratosform, elegircontrato, clienteformhorarios, filtrarinteracciones, filtrarusuarios, subirfoto
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .serializers import contratosserializer, dispositivosserializer, filtrosserializer, usuariosserializer, horariosserializer, interaccionesserializer, fotosserializer, telegramidserializer, aperturaserializer, registroserializer, loginserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
directorio = '/home/ivan/Desktop/appdocker'
# def interaccionesss(request):
#     interaccioness = []
#     interaccionesss= []
#     usuarioss = []
#     contratoo= None
#     cedulafiltro=None
#     fechadesdefiltro=None
#     fechahastafiltro=None
#     horadesdefiltro=None
#     horahastafiltro=None
#     cantidadusuarios=0
#     cantidadinteracciones=0

#     if request.method == "POST":
#         select=elegircontrato(request.POST)
#         filtro=filtrarinteracciones(request.POST)

#         if select.is_valid():
#             contratoo=select.cleaned_data.get('contrato')
#             contratoinstancia = contratos.objects.get(nombre=contratoo)
#             usuarioss = contratoinstancia.contrato.all()

#         if filtro.is_valid():
#             cedulafiltro=filtro.cleaned_data.get('cedula')
#             fechadesdefiltro=filtro.cleaned_data.get('fechadesde')
#             fechahastafiltro=filtro.cleaned_data.get('fechahasta')
#             horadesdefiltro=filtro.cleaned_data.get('horadesde')
#             horahastafiltro=filtro.cleaned_data.get('horahasta')
#             select=elegircontrato({'contrato': contratoo})

#         if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo)


#         if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__gte=fechadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__lte=fechahastafiltro)


#         if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__lte=fechahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro)


#         if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro)


#         if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__gte=fechadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro)


#         if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro)


#         if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__cedula__icontains=cedulafiltro)


#         if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)


#         if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
#             interaccioness = interacciones.objects.filter(contrato=contratoo).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__cedula__icontains=cedulafiltro)

#         interaccionesss = interaccioness[::-1]
#         if cedulafiltro == None and (fechadesdefiltro != None or fechahastafiltro != None or horadesdefiltro != None or horahastafiltro != None):
#             #nombreslista = interaccioness.values_list('nombre', flat=True)
#             cedulaslista = interaccioness.values_list('cedula', flat=True)
#             cedulasunicaslista=[]
#             usuarioss=[]
#             for cedula in cedulaslista:
#                 if not cedula in cedulasunicaslista:
#                     cedulasunicaslista.append(cedula)
#             for cedulaunica in cedulasunicaslista:
#                 usuarioss.append(usuarios.objects.get(cedula=cedulaunica))

#         if cedulafiltro != None and len(interaccioness)>0:
#             cedulaslista = interaccioness.values_list('cedula', flat=True)
#             cedulasunicaslista=[]
#             usuarioss=[]
#             for cedula in cedulaslista:
#                 if not cedula in cedulasunicaslista:
#                     cedulasunicaslista.append(cedula)
#             for cedulaunica in cedulasunicaslista:
#                 usuarioss.append(usuarios.objects.get(cedula=cedulaunica))
#         if cedulafiltro != None and len(interaccioness)==0:
#             usuarioss = []
#         cantidadinteracciones=len(interaccioness)
#         cantidadusuarios=len(usuarioss)

#     else:
#         select=elegircontrato()
#         filtro=filtrarinteracciones()

#     context= {'interaccioness': interaccionesss, 'usuarios':usuarioss, 'contratos':contratoo,'select':select,'filtro':filtro,'cedulafiltro':cedulafiltro,'fechadesdefiltro':fechadesdefiltro,'fechahastafiltro':fechahastafiltro,'horadesdefiltro':horadesdefiltro,'horahastafiltro':horahastafiltro, 'cantidadinteracciones':cantidadinteracciones, 'cantidadusuarios':cantidadusuarios}
#     return render(request, 'web/interacciones.html',context)

# def index(request):
#     return render(request, 'web/index.html')

# def editarcontrato(request, contrato_id):
#     #contratoss = contratos.objects.all()
#     cedulafiltro=None
#     usuarioss = usuarios.objects.filter(contrato=contrato_id)
#     cant1 = len(usuarioss)
#     select=elegircontrato({'contrato': contrato_id})
#     if request.method == 'POST':
#         formcliente = clienteform(request.POST)
#         filtro= filtrarusuarios(request.POST)
#         if filtro.is_valid():
#             cedulafiltro=filtro.cleaned_data.get('cedulaf')
#             if cedulafiltro!=None:
#                 usuarioss = usuarios.objects.filter(cedula__contains=cedulafiltro)
#         if formcliente.is_valid():
#             formcliente.save()

#     else:
#         formcliente = clienteform({'contrato': contrato_id})
#         filtro = filtrarusuarios()
#         usuarioss = usuarios.objects.filter(contrato=contrato_id)

#     if cedulafiltro==None:
#         usuarioss = usuarios.objects.filter(contrato=contrato_id)

#     cantidadusuarios = len(usuarioss)
#     context = {'formcliente' : formcliente, 'usuarios':usuarioss, 'contrato':contrato_id,'select':select, 'filtro':filtro, 'cantidad':cantidadusuarios, 'cedulafiltro':cedulafiltro} #'usuarios':usuarioss,


#     if len(usuarios.objects.filter(contrato=contrato_id)) != cant1 and cedulafiltro==None:
#         return redirect(f'/editarcontrato/{contrato_id}')

#     return render(request, 'web/editarcontrato.html', context)

# def eliminarusuario(request, cedula_id):
#     usuario = usuarios.objects.get(cedula=cedula_id)
#     contrato = usuario.contrato
#     usuario.delete()

#     return redirect(f'/editarcontrato/{contrato}')

# def editarusuario(request, cedula_id):
#     usuario = usuarios.objects.get(cedula=cedula_id)
#     datos = horariospermitidos.objects.filter(cedula=cedula_id)
#     foto = fotos.objects.filter(cedula__cedula__icontains=cedula_id)
#     if foto:
#         foto = foto[0]
#     if request.method == 'POST':
#         formclientehorarios = clienteformhorarios(request.POST)
#         formfoto = subirfoto(request.POST, request.FILES)
#         if formclientehorarios.is_valid():
#             formclientehorarios.save()
#         if formfoto.is_valid():
#             formfoto.save()
#             foto = fotos.objects.filter(cedula__cedula__icontains=cedula_id)
#             if foto:
#                 foto = foto[0]
#             #imagen = formfoto.cleaned_data['img']

#     else:
#         formclientehorarios = clienteformhorarios({'cedula': cedula_id})
#         formfoto = subirfoto({'cedula': cedula_id})

#     context = {'usuario':usuario, 'datos': datos, 'formclientehorarios':formclientehorarios, 'formfoto':formfoto, 'foto':foto}
#     return render(request, 'web/editarusuario.html', context)

# def eliminarhorario(request, id_web):
#     horario = horariospermitidos.objects.get(id=id_web)
#     cedula_id = horario.cedula.cedula
#     horario.delete()

#     return redirect(f'/editarusuario/{cedula_id}')

# def agregarcontrato(request):
#     contratoss = contratos.objects.all()
#     if request.method == 'POST':
#         formcontrato = contratosform(request.POST)
#         if formcontrato.is_valid():
#             formcontrato.save()
#     else:
#         formcontrato = contratosform()

#     context = {'formcontrato' : formcontrato, 'contratos': contratoss}

#     return render(request, 'web/agregarcontrato.html', context)

# def eliminarcontrato(request, contrato_id):
#     contrato = contratos.objects.get(nombre=contrato_id)
#     usuarioscontrato = usuarios.objects.filter(contrato=contrato_id)
#     foto = None
#     for usuariofoto in usuarioscontrato:
#         usuariocedula = usuariofoto.cedula
#         foto = fotos.objects.filter(cedula__cedula__icontains=usuariocedula)
#         if len(foto) > 0:
#             foto=foto[0]
#             foto.foto.delete(save=False)
#     contrato.delete()

#     return redirect('agregarcontrato')

# def eliminarfoto(request, cedula_id):
#     foto = fotos.objects.get(cedula=cedula_id)
#     foto.foto.delete(save=False)
#     foto.delete()

#     return redirect(f'/editarusuario/{cedula_id}')


# def seleccionarcontrato(request):
#     if request.method == "POST":
#         select=elegircontrato(request.POST)
#         if select.is_valid():
#             contratoo=select.cleaned_data.get('contrato')
#     else:
#         select=elegircontrato()
#         contratoo=None
#     #cont= request.GET['contrato']
#     #'usuarios':usuarioss,
#     usuarioss = usuarios.objects.filter(contrato=contratoo)
#     cantidadusuarios = len(usuarioss)
#     context = {'select':select, 'contrato':contratoo, 'usuarios':usuarioss, 'cantidad':cantidadusuarios}
#     return render(request, 'web/seleccionarcontrato.html', context)



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

#@csrf_exempt
#@ensure_csrf_cookie
def agregarcontratosapi(request):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
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
                    #response = JsonResponse(contrato_serializer.data, status=status.HTTP_201_CREATED)
                    #response['X-CSRFToken'] = 'ybrW4cFaoZ4zSSHApb9hH7Dxaqgd2rkx5dxST8mbysSr3ebrFYIi74JiAN5nDyx5'
                    #return response
                else:
                    return JsonResponse(contrato_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)


#@csrf_exempt
def eliminarcontratos(request, contrato_id):
    #contrato_id = contrato_id.replace("%20", " ")
    usuarios_filter=[]
    fotos_filter=[]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'DELETE':
                usuarios_filter = usuarios.objects.filter(contrato=contrato_id)
                for usuario in usuarios_filter:
                    id_usuario = usuario.id
                    fotos_filter = fotos.objects.filter(usuario=id_usuario)
                    if fotos_filter:
                        for foto in fotos_filter:
                            foto.foto.delete(save=False)
                            foto.delete()
                contrato=contratos.objects.get(nombre=contrato_id)
                contrato.delete()
                return JsonResponse({'eliminado': True}, status=200)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)




#@csrf_exempt
def seleccionarcontratoapi(request, contrato_id):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'POST':
                usuarioscontrato = usuarios.objects.filter(contrato=contrato_id)
                usuarioscontrato_serializer = usuariosserializer(usuarioscontrato, many=True)
                return JsonResponse(usuarioscontrato_serializer.data, safe=False)
                # contratoseleccionado_data = JSONParser().parse(request)
                # contratoselecserializer = stringserializer(contratoseleccionado_data)
                #contratoselecserializer.data
                # if contrato_serializer.is_valid():
                    #return JsonResponse(contrato_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)

def dispositivosapi(request, contrato_id):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'POST':
                dispositivoscontrato = dispositivos.objects.filter(contrato=contrato_id).exclude(descripcion='SERVIDOR LOCAL')
                dispositivoscontrato_serializer = dispositivosserializer(dispositivoscontrato, many=True)
                return JsonResponse(dispositivoscontrato_serializer.data, safe=False)
                # contratoseleccionado_data = JSONParser().parse(request)
                # contratoselecserializer = stringserializer(contratoseleccionado_data)
                #contratoselecserializer.data
                # if contrato_serializer.is_valid():
                    #return JsonResponse(contrato_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)

def servidorlocal(request, contrato_id):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'POST':
                servidorlocalcontrato = dispositivos.objects.filter(contrato=contrato_id).filter(descripcion='SERVIDOR LOCAL')
                if servidorlocalcontrato:
                    servidorlocalcontrato = servidorlocalcontrato[0]
                    #servidorlocalcontrato_serializer = dispositivosserializer(servidorlocalcontrato, many=False)
                    return JsonResponse({'SERVIDOR_LOCAL': servidorlocalcontrato.estado}, safe=False)
                else:
                    return JsonResponse({'SERVIDOR_LOCAL': '2'}, safe=False)

                # contratoseleccionado_data = JSONParser().parse(request)
                # contratoselecserializer = stringserializer(contratoseleccionado_data)
                #contratoselecserializer.data
                # if contrato_serializer.is_valid():
                    #return JsonResponse(contrato_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)

def probar_conexion_servidorlocal(request, contrato_id):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'POST':
                servidorlocalcontrato = dispositivos.objects.filter(contrato=contrato_id).filter(descripcion='SERVIDOR LOCAL')
                if servidorlocalcontrato:
                    servidorlocalcontrato = servidorlocalcontrato[0]
                    servidorlocalcontrato.estado = '0'
                    servidorlocalcontrato.save(update_fields=['estado'])
                    return JsonResponse({'detail': 'comprobando conexion con el serviodor local'}, safe=False)
                else:
                    return JsonResponse({'detail': 'Aun no existe un servidor local en el contrato'}, safe=False)
                # contratoseleccionado_data = JSONParser().parse(request)
                # contratoselecserializer = stringserializer(contratoseleccionado_data)
                #contratoselecserializer.data
                # if contrato_serializer.is_valid():
                    #return JsonResponse(contrato_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)



#@csrf_exempt
def agregarusuarioapi(request):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'POST':
                usuario_data = JSONParser().parse(request)
                usuario_serializer = usuariosserializer(data=usuario_data)
                usuario_cedula=usuario_serializer.initial_data.get('cedula', None)
                nombre_cedula=usuario_serializer.initial_data.get('nombre', None)
                usuario_contrato=usuario_serializer.initial_data.get('contrato', None)
                usuario_modelo=usuarios.objects.filter(contrato=usuario_contrato, cedula=usuario_cedula)
                if usuario_modelo:
                    return JsonResponse({'usuario_añadido':False, 'nombre':nombre_cedula}, status=200)
                else:
                    if usuario_serializer.is_valid():
                        usuario_serializer.save()
                        return JsonResponse({'usuario_añadido':True, 'nombre':nombre_cedula}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)

#@csrf_exempt
def agregartelegramidapi(request):
    telegram_id=None
    cedula_id=None

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'POST':
                telegramid_data = JSONParser().parse(request)
                telegramid_serializer = telegramidserializer(data=telegramid_data)
                telegram_id=telegramid_serializer.initial_data.get('telegram_id', None)
                cedula_id=telegramid_serializer.initial_data.get('cedula', None)
                if telegramid_serializer.is_valid():
                    instancia_usuario = usuarios.objects.filter(cedula=cedula_id)
                    instancia_usuario = instancia_usuario[0]
                    if str(telegram_id) != '0':
                        instancia_usuario.telegram_id = str(telegram_id)
                        instancia_usuario.save(update_fields=['telegram_id'])
                        return JsonResponse(telegramid_serializer.data, status=status.HTTP_201_CREATED)
                    if str(telegram_id) == '0':
                        telegram_id = ''
                        instancia_usuario.telegram_id = telegram_id
                        instancia_usuario.save(update_fields=['telegram_id'])
                        return JsonResponse(telegramid_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(telegramid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if request.method == 'DELETE':
                telegramid_data = JSONParser().parse(request)
                telegramid_serializer = telegramidserializer(data=telegramid_data)
                telegram_id=telegramid_serializer.initial_data.get('telegram_id', None)
                cedula_id=telegramid_serializer.initial_data.get('cedula', None)
                if telegramid_serializer.is_valid():
                    instancia_usuario = usuarios.objects.filter(cedula=cedula_id)
                    instancia_usuario = instancia_usuario[0]
                    if str(telegram_id) == '0':
                        telegram_id=None
                    instancia_usuario.telegram_id = telegram_id
                    instancia_usuario.save(update_fields=['telegram_id'])
                    return JsonResponse(telegramid_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(telegramid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)


#@csrf_exempt
def eliminarusuarioapi(request, cedula_id):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'DELETE':
                usuario=usuarios.objects.get(id=cedula_id)
                usuario.delete()
                return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)


#@csrf_exempt
def buscarusuarioapi(request, cedula_id):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'GET':
                usuarioss=usuarios.objects.filter(cedula__icontains=cedula_id)
                usuarioss_serializer = usuariosserializer(usuarioss, many=True)
                # if len(usuarioss) == 1:
                #     usuarioss=usuarioss[0]
                #     usuarioss_serializer = usuariosserializer(usuarioss, many=True)
                return JsonResponse(usuarioss_serializer.data, safe=False)

            if request.method == 'POST':
                contrato_data = JSONParser().parse(request)
                contrato_serializer = contratosserializer(data=contrato_data)
                contratofiltro= contrato_serializer.initial_data.get('nombre', None)
                usuarioss=usuarios.objects.filter(cedula__icontains=cedula_id, contrato=contratofiltro)
                usuarioss_serializer = usuariosserializer(usuarioss, many=True)
                # if len(usuarioss) == 1:
                #     usuarioss=usuarioss[0]
                #     usuarioss_serializer = usuariosserializer(usuarioss, many=True)
                return JsonResponse(usuarioss_serializer.data, safe=False)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)


#@csrf_exempt
def editarhorariosapi(request, cedula_id):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'GET':
                horarios = horariospermitidos.objects.filter(cedula=cedula_id)
                horarios_serializer = horariosserializer(horarios, many=True)
                return JsonResponse(horarios_serializer.data, safe=False)

            elif request.method == 'POST':
                horarios_data = JSONParser().parse(request)
                horarios_serializerr = horariosserializer(data=horarios_data)
                if horarios_serializerr.is_valid():
                    horarios_serializerr.save()
                    return JsonResponse(horarios_serializerr.data, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(horarios_serializerr.errors, status=status.HTTP_400_BAD_REQUEST)

            elif request.method == 'DELETE':
                horario=horariospermitidos.objects.get(id=cedula_id)
                horario.delete()
                return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)


#@csrf_exempt
def editarfotosapi(request, cedula_id):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            if request.method == 'GET':
                #foto = fotos.objects.filter(cedula__cedula__icontains=cedula_id)
                foto = fotos.objects.filter(cedula__icontains=cedula_id)
                foto_serializer = fotosserializer(foto, many=True)
                return JsonResponse(foto_serializer.data, safe=False)
            elif request.method == 'DELETE':
                foto = fotos.objects.get(id=cedula_id)
                foto.foto.delete(save=False)
                foto.delete()
                return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)



class agregarfoto(viewsets.ModelViewSet):
    parser_class = (FileUploadParser,)
    queryset = fotos.objects.all()
    serializer_class = fotosserializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(agregarfoto, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.admin:
                file_serializer = fotosserializer(data=request.data)

                if file_serializer.is_valid():
                    file_serializer.save()
                    return Response(file_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
        else:
            return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)


#id = serializer.data.get('id', None)
#@csrf_exempt
def interaccionesapi(request):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    if request.user.is_authenticated:
        if request.user.admin:
            interaccioness = []
            interaccionesss= []
            usuarioss = []
            contratofiltro= None
            cedulafiltro=None
            fechadesdefiltro=None
            fechahastafiltro=None
            horadesdefiltro=None
            horahastafiltro=None


            if request.method == 'POST': 
                filtros_data = JSONParser().parse(request)
                filtros_serializer = filtrosserializer(data=filtros_data)
                contratofiltro= filtros_serializer.initial_data.get('contrato', None)
                cedulafiltro= filtros_serializer.initial_data.get('cedula', None)
                fechadesdefiltro=filtros_serializer.initial_data.get('fechadesde', None)
                fechahastafiltro=filtros_serializer.initial_data.get('fechahasta', None)
                horadesdefiltro=filtros_serializer.initial_data.get('horadesde', None)
                horahastafiltro=filtros_serializer.initial_data.get('horahasta', None)


                if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(fecha__gte=fechadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(fecha__lte=fechahastafiltro)


                if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__gte=horadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__gte=horadesdefiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro)


                if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro)


                if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(fecha__gte=fechadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro)


                if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro == None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro == None and horadesdefiltro != None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro)


                if cedulafiltro != None and fechadesdefiltro == None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(cedula__icontains=cedulafiltro)


                if cedulafiltro == None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro)


                if cedulafiltro != None and fechadesdefiltro != None and fechahastafiltro != None and horadesdefiltro != None and horahastafiltro != None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro).filter(hora__lte=horahastafiltro).filter(hora__gte=horadesdefiltro).filter(fecha__lte=fechahastafiltro).filter(fecha__gte=fechadesdefiltro).filter(cedula__icontains=cedulafiltro)

                interaccionesss = interaccioness[::-1]

                if cedulafiltro == None and fechadesdefiltro == None and fechahastafiltro == None and horadesdefiltro == None and horahastafiltro == None:
                    interaccioness = interacciones.objects.filter(contrato=contratofiltro)
                    interaccionesss = interaccioness[::-1]
                    #interaccionesss = interaccionesss[:15]
                #interacciones_data = interacciones.objects.filter(cedula__cedula__icontains=cedulafiltro)
                interacciones_serializer = interaccionesserializer(interaccionesss, many=True) 
                #return HttpResponse(cedulaapi)
                return JsonResponse(interacciones_serializer.data, safe=False)
        else:
            return JsonResponse({'detail': 'Usuario sin los permisos requeridos.'}, status=400)
    else:
        return JsonResponse({'detail': 'No hay un usuario logueado.'}, status=400)

#id = serializer.data.get('id', None)

#@csrf_exempt
@api_view(['GET', 'POST'])
def aperturaa(request):

    if request.method == 'GET': 
        aperturainfo = apertura.objects.all()
        apertura_serializer = aperturaserializer(aperturainfo, many=True)
        return JsonResponse(apertura_serializer.data, safe=False)

    elif request.method == 'POST':
        instancia_apertura = apertura.objects.get(id=0)
        aperturapost_serializer = aperturaserializer(instancia_apertura, data=request.data)
        if aperturapost_serializer.is_valid():
            aperturapost_serializer.save()
            return JsonResponse(aperturapost_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(aperturapost_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class registrarusuario(viewsets.ModelViewSet):
#     serializer_class = registroserializer
#     queryset = User.objects.all()

#     def post(self, request, *args, **kwargs):
#         user_serializer = registroserializer(data=request.data)

#         cedula= user_serializer.initial_data.get('cedula', None)
#         email= user_serializer.initial_data.get('email', None)
#         cedulabuscar = User.objects.filter(cedula=cedula)
#         emailbuscar = User.objects.filter(email=email)
#         if user_serializer.is_valid() and not emailbuscar and not cedulabuscar:
#             user_serializer.save()
#             return Response({'cuenta creada': True}, status=201)
#         elif emailbuscar or cedulabuscar:
#             return Response({'cuenta creada': False}, status=200)

    
def registraruser(request):

    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = registroserializer(data=user_data)
        cedula= user_serializer.initial_data.get('cedula', None)
        email= user_serializer.initial_data.get('email', None)
        cedulabuscar = User.objects.filter(cedula=cedula)
        emailbuscar = User.objects.filter(email=email)
        if user_serializer.is_valid() and not emailbuscar and not cedulabuscar:
            user_serializer.save()
            return JsonResponse({'cedula':False,
                                 'email':False,
                                 'cuenta_creada': True}, status=201)
        elif emailbuscar and cedulabuscar:
            return JsonResponse({'cedula':True,
                                 'email':True,
                                 'cuenta_creada': False}, status=200)
        elif emailbuscar and not cedulabuscar:
            return JsonResponse({'cedula':False,
                                 'email':True,
                                 'cuenta_creada': False}, status=200)
        elif cedulabuscar and not emailbuscar:
            return JsonResponse({'cedula':True,
                                 'email':False,
                                 'cuenta_creada': False}, status=200)

def index(request, path=''):
    """
    Renders the Angular2 SPA
    """
    return render(request, 'index.html')


#@csrf_exempt 
#@api_view(['GET'])
#@ensure_csrf_cookie
def get_csrf(request):
    if request.method == 'GET':
        get_token(request)
        return JsonResponse({'detail': 'CSRF cookie set'}, status=200)

#@ensure_csrf_cookie
#@csrf_exempt
def loginapi(request):

    if request.method == 'POST':
        login_data = JSONParser().parse(request)
        login_serializer = loginserializer(data=login_data)
        if login_serializer.is_valid():
            cedula= login_serializer.initial_data.get('cedula', None)
            passwordd= login_serializer.initial_data.get('password', None)

            if cedula is None or passwordd is None:
                return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

            user = authenticate(username=cedula, password=passwordd)

            if user is None:
                return JsonResponse({'cedula': 'Invalid credentials',
                                 #'is_active':request.user.is_active,
                                 'staff': False,
                                 'admin': False,
                                 'authenticated': False}, status=200)

            login(request, user)
            get_token(request)
            return JsonResponse({'cedula': user.cedula,
                                 #'is_active':request.user.is_active,
                                 'staff': user.staff,
                                 'admin': user.admin,
                                 'authenticated': user.is_authenticated}, status=200)



def logoutapi(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)
        logout(request)
        return JsonResponse({'detail': 'Successfully logged out.'}, status=200)


class SessionView(APIView):
    @staticmethod
    def get(request, format=None):
        if request.user.is_authenticated:
            return JsonResponse({'cedula': request.user.cedula, 
                                 #'is_active':request.user.is_active, 
                                 'staff':request.user.staff, 
                                 'admin':request.user.admin,
                                 'authenticated': request.user.is_authenticated})
        else:
            return JsonResponse({'cedula': '', 
                                 #'is_active': False, 
                                 'staff': False, 
                                 'admin': False,
                                 'authenticated': False})


class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    #@login_required
    #@login_required(login_url="loginn")
    @staticmethod
    def get(request, format=None):
        return JsonResponse({'cedula': request.user.cedula, 'is_active':request.user.is_active, 'staff':request.user.staff, 'admin':request.user.admin})













# def get_csrf(request):
#     response = JsonResponse({'detail': 'CSRF cookie set'})
#     response['X-CSRFToken'] = get_token(request)
#     return response


# @require_POST
# def login_view(request):
#     data = json.loads(request.body)
#     username = data.get('username')
#     password = data.get('password')

#     if username is None or password is None:
#         return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

#     user = authenticate(username=username, password=password)

#     if user is None:
#         return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

#     login(request, user)
#     return JsonResponse({'detail': 'Successfully logged in.'})


# def logout_view(request):
#     if not request.user.is_authenticated:
#         return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

#     logout(request)
#     return JsonResponse({'detail': 'Successfully logged out.'})


# class SessionView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     @staticmethod
#     def get(request, format=None):
#         return JsonResponse({'isAuthenticated': True})


# class WhoAmIView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     @staticmethod
#     def get(request, format=None):
#         return JsonResponse({'username': request.user.username})