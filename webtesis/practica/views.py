from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse


def abr(request):
    return HttpResponse('pruebaxd')
def abr2(request):
    return HttpResponse('prueba2xd')

 #para mostrar variables de la request
def pruebavariable(request, variable):
    return HttpResponse(f'la variable es: {variable}')

#para solo mostrar archivos html
def archivohtml(request):
    return render(request, 'practica/index.html')

#para mostrar variables de la request en un archivo html
def archivohtml2(request, variablehtml):
    context = {'variable':variablehtml}
    return render(request, 'practica/practica2.html', context)

def archivohtml3(request, variablehtml2):
    variablehtml2=2
    context = {'variable3':variablehtml2}
    return render(request, 'practica/logicaenhtml.html', context)