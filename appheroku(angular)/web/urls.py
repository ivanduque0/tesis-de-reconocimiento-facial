from django.urls import path, include, re_path
from . import views
from .views import agregarfoto, registrarusuario, SessionView
from rest_framework import routers
from django.views.generic import RedirectView

# router = routers.DefaultRouter()
# router.register(r'contratos', views.ContratosList)

router = routers.DefaultRouter()
router.register(r'subirfotos', views.agregarfoto)
router.register(r'registro', views.registrarusuario)

urlpatterns = [
    path('api', include(router.urls)),
    re_path(r'^agregarcontratosapi/$', views.agregarcontratosapi),
    re_path(r'^removercontratosapi/(?P<contrato_id>[\w\ ]+)/$', views.eliminarcontratos),
    re_path(r'^seleccionarcontratoapi/(?P<contrato_id>[\w\ ]+)/$', views.seleccionarcontratoapi),
    re_path(r'^editcontrato/agregarusuario/$', views.agregarusuarioapi),
    re_path(r'^editcontrato/eliminarusuario/(?P<cedula_id>[\w\ ]+)/$', views.eliminarusuarioapi),
    re_path(r'^editcontrato/buscarusuario/(?P<cedula_id>[\w\ ]+)/$', views.buscarusuarioapi),
    re_path(r'^editusuario/horarios/(?P<cedula_id>[\w\ ]+)/$', views.editarhorariosapi),
    re_path(r'^editusuario/foto/(?P<cedula_id>[\w\ ]+)/$', views.editarfotosapi),
    re_path(r'^editusuario/agregarid/$', views.agregartelegramidapi),
    re_path(r'^actividad/$', views.interaccionesapi),
    re_path(r'^apertura/$', views.aperturaa),
    re_path(r'^loginapi/$', views.loginapi, name='api-login'),
    path('logout/', views.logoutapi, name='api-logout'),
    path('csrf/', views.get_csrf, name='api-csrf'),
    path('session/', SessionView.as_view(), name='api-session'),
    re_path(r'^(?P<path>.*)/$', views.index),
]   