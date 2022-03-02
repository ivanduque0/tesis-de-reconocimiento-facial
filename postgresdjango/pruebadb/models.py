from django.db import models
from django.forms import IntegerField

# Create your models here.

class empresa(models.Model):
    nombre = models.CharField(max_length=20)
    fundacion=models.IntegerField()
    #con esto se logra que en el panel de administracion
    #se nos muestren directamente los datos de la tabla
    #sin necesidad de primero entrar

    def __str__(self):
        return self.nombre, self.fundacion

class interacciones(models.Model):
    nombre= models.CharField(max_length=50)
    fecha= models.DateField()
    hora= models.TimeField()
    razon= models.CharField(max_length=20)
    def __str__(self):
        #return self.nombre, self.fecha, self.hora, self.razon
        return self.nombre

class programador(models.Model):
    nombre= models.CharField(max_length=50)
    #con eso de ondelete=models.CASCADE lo que se hace
    #es que debido a que es una llave foranea de otro modelo, 
    #si se elimina el item al que esta asociada la lllave foranea
    #automaticamente se eliminan los items de esta lista asociados
    #al item que se elimino en la otra tabla y que en esta tabla 
    #es una llave foranea
    empresa= models.ForeignKey(empresa, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre