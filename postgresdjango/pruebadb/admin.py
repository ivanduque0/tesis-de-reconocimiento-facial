from django.contrib import admin
from .models import empresa, programador, interacciones

# Register your models here.

admin.site.register(empresa)
admin.site.register(interacciones)
admin.site.register(programador)

