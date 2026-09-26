from rest_framework import serializers
from .models import Usuario, Descarte, Destino

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class DescarteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descarte
        fields = '__all__'

class DestinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destino
        fields = '__all__'
