from hashlib import new
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.http import HttpResponse
from .models import contratos, dispositivos, fotos, horariospermitidos, interacciones, usuarios, apertura, User
#from .forms import clienteform, contratosform, elegircontrato, clienteformhorarios, filtrarinteracciones, filtrarusuarios, subirfoto
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .serializers import contratosserializer, dispositivosserializer,filtrosserializer, usuariosserializer, horariosserializer, interaccionesserializer, fotosserializer, telegramidserializer, aperturaserializer, registroserializer, loginserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

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


def eliminarcontratos(request, contrato_id):
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
                    interaccionesss = interaccionesss[:100]
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

def get_csrf(request):
    if request.method == 'GET':
        get_token(request)
        return JsonResponse({'detail': 'CSRF cookie set'}, status=200)

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
