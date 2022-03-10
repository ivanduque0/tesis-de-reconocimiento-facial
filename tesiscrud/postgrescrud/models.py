from django.db import models
# Create your models here.

class contratos(models.Model):
    #el verbose_name sirve para el nombre que se le dara en el panel de administracion
    nombre= models.CharField(primary_key=True, max_length=100, verbose_name='nombre del nuevo contrato')
    class Meta:
        # con esto se ltera el nombre que se la da a cada clae en el panel de administracion
        verbose_name_plural = "Contratos"
    def __str__(self):
        return self.nombre

class usuarios(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    contrato = models.ForeignKey(contratos, on_delete = models.CASCADE, related_name='contrato', verbose_name='contratousuarios') #models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Usuarios"

    #def __str__(self):
    #    return self.cedula

class interacciones(models.Model):
    cedula = models.ForeignKey(usuarios, db_constraint=False, on_delete = models.DO_NOTHING, related_name='cedulainteracciones') #models.IntegerField()
    nombre = models.CharField(max_length=50)
    fecha = models.DateField()
    hora = models.TimeField()
    razon = models.CharField(max_length=20)
    contrato = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Interacciones"
    #def __str__(self):
        #return self.cedula,self.nombre, self.fecha, self.hora, self.razon
        #return self.nombre

class diasdelasemana(models.Model):
    dia=models.CharField(primary_key=True, max_length=20)
    class Meta:
        verbose_name_plural = "Dias de la semana"
    def __str__(self):
        return self.dia

class horariospermitidos(models.Model):
    cedula = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="ceduladiaspermitidos")
    dia=models.ForeignKey(diasdelasemana, db_constraint=False, on_delete = models.DO_NOTHING, related_name='diadelasemana')
    entrada=models.TimeField()
    salida=models.TimeField()
    class Meta:
        verbose_name_plural = "Horarios"
        