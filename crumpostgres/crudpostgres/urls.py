from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('agregar', views.agregarusuario, name='agregar'),
    path('eliminar/<int:cedula_id>/', views.eliminarusuario, name='eliminar'),
]

