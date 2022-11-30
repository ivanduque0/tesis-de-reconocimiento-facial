from django.urls import path, include, re_path
from . import views
from .views import agregarfoto, SessionView, Mobilecontratosapi
from rest_framework import routers
from django.views.generic import RedirectView

# router = routers.DefaultRouter()
# router.register(r'contratos', views.ContratosList)

router = routers.DefaultRouter()
router.register(r'subirfotos', views.agregarfoto)

urlpatterns = [
    path('api', include(router.urls)),
    re_path(r'^mobilecontratosapi/$', Mobilecontratosapi.as_view()),
    re_path(r'^agregarcontratosapi/$', views.agregarcontratosapi),
    re_path(r'^removercontratosapi/(?P<contrato_id>[\w\ ]+)/$', views.eliminarcontratos),
    re_path(r'^seleccionarcontratoapi/(?P<contrato_id>[\w\ ]+)/$', views.seleccionarcontratoapi),
    re_path(r'^editcontrato/agregarusuario/$', views.agregarusuarioapi),
    re_path(r'^editcontrato/eliminarusuario/(?P<usuario_id>[\w\ ]+)/$', views.eliminarusuarioapi),
    re_path(r'^dispositivosapi/(?P<contrato_id>[\w\ ]+)/$', views.dispositivosapi),
    re_path(r'^servidorlocalapi/(?P<contrato_id>[\w\ ]+)/$', views.servidorlocal),
    re_path(r'^probarservidorlocalapi/(?P<contrato_id>[\w\ ]+)/$', views.probar_conexion_servidorlocal),
    re_path(r'^editcontrato/buscarusuario/(?P<cedula_id>[\w\ ]+)/$', views.buscarusuarioapi),
    re_path(r'^editusuario/huellasapi/(?P<cedula_id>[\w\ ]+)/$', views.huellasapi),
    re_path(r'^editusuario/tagsrfidapi/(?P<cedula_id>[\w\ ]+)/$', views.tagsrfidapi),
    re_path(r'^editusuario/horarios/(?P<cedula_id>[\w\ ]+)/$', views.editarhorariosapi),
    re_path(r'^editusuario/foto/(?P<cedula_id>[\w\ ]+)/$', views.editarfotosapi),
    re_path(r'^editusuario/agregarid/$', views.agregartelegramidapi),
    re_path(r'^actividad/$', views.interaccionesapi),
    re_path(r'^apertura/$', views.aperturaa),
    re_path(r'^loginapi/$', views.loginapi, name='api-login'),
    path('logout/', views.logoutapi, name='api-logout'),
    path('csrf/', views.get_csrf, name='api-csrf'),
    path('session/', SessionView.as_view(), name='api-session'),
    path('apiregistro/', views.registraruser),
    re_path(r'^(?P<path>.*)/$', views.index),
]   