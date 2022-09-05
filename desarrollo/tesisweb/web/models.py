from enum import unique
from django.db import models  
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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
    #cedula = models.IntegerField(primary_key=True)
    cedula = models.CharField(max_length=150,primary_key=False)
    # Es mejor si es charfield y si no es llave primaria
    # ya que quizas seria bueno que se pudieran agregar 
    # mismos usuarios a distintos contratos para los tecnicos
    # o personas que podrian vivir en dos residencias similares
    # sin embargo si se hace esto, lo que se debera poner y lo que se obtendra 
    # en las llaves foraneas sera el id, es decir, la primary key del modelo
    nombre = models.CharField(max_length=150)
    contrato = models.ForeignKey(contratos, on_delete = models.CASCADE, related_name='contrato', verbose_name='contratousuarios') #models.CharField(max_length=100)
    telegram_id = models.CharField(max_length=150, blank=True) 
    
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

class horariospermitidos(models.Model):

    class dias(models.TextChoices):
        LUNES = 'Lunes', 'Lunes'
        MARTES = 'Martes', 'Martes'
        MIERCOLES = 'Miercoles','Miercoles'
        JUEVES = 'Jueves', 'Jueves'
        VIERNES = 'Viernes', 'Viernes'
        SABADO = 'Sabado', 'Sabado'
        DOMINGO = 'Domingo', 'Domingo'
        SIEMPRE = 'Siempre', 'Siempre'

    # en este campo se debe poner el "id" del usuario, no la cedula
    usuarioid = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="ceduladiaspermitidos")
    dia=models.CharField(max_length=20, choices=dias.choices, default=dias.LUNES)
    contrato = models.ForeignKey(contratos, on_delete = models.CASCADE, related_name='contratohorarios', verbose_name='contratodiaspermitidos')
    entrada=models.TimeField()
    salida=models.TimeField()
    class Meta:
        verbose_name_plural = "Horarios"

class fotos(models.Model):
    cedula = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="cedulafoto")
    foto = models.ImageField(upload_to='personas/')
    estado = models.IntegerField()

class apertura(models.Model):
    contrato = models.CharField(max_length=50)
    acceso = models.CharField(max_length=50)






class UserManager(BaseUserManager):
    def create_user(self, cedula, email, password):
        
        if not email or not cedula:
            raise ValueError('El usuario debe tener un correo valido y una cedula')

        user = self.model(
            cedula=cedula,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, email, password):
        
        if not email or not cedula:
            raise ValueError('El usuario debe tener un correo valido y una cedula')

        user = self.create_user (
            cedula,
            email,
            password=password
        )
        user.staff = True
        user.admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    cedula = models.CharField(max_length=200, unique = True)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'cedula'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email','password']
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
    
    objects = UserManager()