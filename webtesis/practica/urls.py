from django.urls import path
from . import views

urlpatterns = [
    #asi se usa para hacer rutas estaticas, es decir
    #lo que se ponga en las funciones va a aparecer tal cual
    path('', views.abr, name='xddd'),
    path('abr2/', views.abr2, name='xddd2'),
    #asi se hace para rutas dinamicas, es decir, se pueden pasar variables
    #y esas variable van a interaccionar con la web
    path('<str:variable>', views.pruebavariable, name='variable'),
    #asi se hace para mostrar archivos html al hacer una request
    path('pruebahtml/', views.archivohtml, name='htmlxd'),
    path('pruebahtml2/<str:variablehtml>', views.archivohtml2, name='html2xd'),
    path('pruebahtml3/<str:variablehtml2>', views.archivohtml3, name='html3xd'),
]