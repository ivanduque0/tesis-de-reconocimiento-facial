from rest_framework import serializers 
from .models import contratos, fotos, horariospermitidos, interacciones, usuarios, apertura, User
 
class contratosserializer(serializers.ModelSerializer):
 
    class Meta:
        model= contratos
        fields = ['nombre']

class usuariosserializer(serializers.ModelSerializer):
 
    class Meta:
        model = usuarios
        fields = '__all__'
        #fields = ['cedula', 'nombre', 'contrato', 'telegram_id']

class horariosserializer(serializers.ModelSerializer):
 
    class Meta:
        model = horariospermitidos
        fields = '__all__'
        #fields = ['id', 'cedula', 'dia', 'entrada', 'salida', 'contrato']

class interaccionesserializer(serializers.ModelSerializer):

    class Meta:
        model= interacciones
        fields = '__all__'
        # fields = ['cedula','nombre','fecha','hora','razon','contrato','usuario']

class fotosserializer(serializers.ModelSerializer):

    class Meta:
        model = fotos
        fields = '__all__'
        #fields = ['id','cedula', 'foto', 'estado','usuario']

class filtrosserializer(serializers.Serializer):
    cedula = serializers.IntegerField()
    contrato = serializers.CharField()
    fechadesde = serializers.DateField()
    fechahasta = serializers.DateField()
    horadesde = serializers.TimeField()
    horahasta = serializers.TimeField()

class telegramidserializer(serializers.Serializer):
    cedula = serializers.IntegerField()
    telegram_id = serializers.CharField()

class aperturaserializer(serializers.ModelSerializer):
    class Meta:
        model = apertura
        fields = '__all__'
        
# class stringserializer(serializers.Serializer):
#     string = serializers.CharField(max_length=200)


class usuariosregistroserializer(serializers.Serializer):
    
    cedula=serializers.IntegerField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def create(self, validate_data):
        
        Instance = User()
        Instance.cedula = validate_data.get('cedula')
        Instance.email = validate_data.get('email')
        # Instance.nombre = validate_data.get('nombre')
        # Instance.apellido = validate_data.get('apellido')
        Instance.set_password(validate_data.get('password'))
        Instance.save()
        return Instance

    def validate_cedula(self, data):
        Usuarios = User.objects.filter(cedula=data)
        if len(Usuarios) != 0:
            raise serializers.ValidationError('Esta cedula ya tiene una cuenta asociada, ingrese uno nuevo')
        else:
            return 
            
class loginserializer(serializers.Serializer):

    class Meta:
        model= User
        fields = ['cedula','password']

class registroserializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields = ['cedula','email','password']

    def create(self, validate_data):
        
        user = User.objects.create_user(**validate_data)
        return user