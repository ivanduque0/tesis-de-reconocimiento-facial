from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('interacciones', views.interaccionesss, name='interacciones'),
    path('editarcontrato/<str:contrato_id>/', views.editarcontrato, name='editarcontrato'),
    path('eliminarusuario/<int:cedula_id>/', views.eliminarusuario, name='eliminarusuario'),
    path('eliminarhorario/<int:id_web>', views.eliminarhorario, name='eliminarhorario'),
    path('editarusuario/<int:cedula_id>', views.editarusuario, name='editarusuario'),
    path('agregarcontrato', views.agregarcontrato, name='agregarcontrato'),
    path('eliminarcontrato/<str:contrato_id>/', views.eliminarcontrato, name='eliminarcontrato'),
    path('editarcontrato', views.seleccionarcontrato, name='seleccionarcontrato'),
]