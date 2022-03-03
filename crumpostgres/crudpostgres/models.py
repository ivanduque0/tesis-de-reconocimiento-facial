from django.db import models
from sqlalchemy import ForeignKey

# Create your models here.

class oficina(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre, self.cedula

class interacciones(models.Model):
    nombre = models.CharField(max_length=50)
    cedula = models.ForeignKey(oficina, on_delete = models.PROTECT, related_name='cedulas')
    fecha = models.DateField()
    hora = models.TimeField()
    razon = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre, self.fecha, self.hora, self.razon
        #return self.nombre

