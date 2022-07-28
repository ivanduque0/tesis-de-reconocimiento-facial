from rest_framework import serializers 
from .models import contratos, fotos, horariospermitidos, interacciones, usuarios, apertura
 
class contratosserializer(serializers.ModelSerializer):
 
    class Meta:
        model= contratos
        fields = ['nombre']

class usuariosserializer(serializers.ModelSerializer):
 
    class Meta:
        model = usuarios
        fields = ['cedula', 'nombre', 'contrato', 'telegram_id']

class horariosserializer(serializers.ModelSerializer):
 
    class Meta:
        model = horariospermitidos
        fields = ['id', 'cedula', 'dia', 'entrada', 'salida']

class interaccionesserializer(serializers.ModelSerializer):

    class Meta:
        model= interacciones
        fields = ['cedula','nombre','fecha','hora','razon','contrato']

class fotosserializer(serializers.ModelSerializer):

    class Meta:
        model = fotos
        fields = ['id','cedula', 'foto', 'estado']

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

