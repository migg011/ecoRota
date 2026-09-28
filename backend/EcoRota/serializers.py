from django.contrib.auth.password_validation import validate_password
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

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = Usuario
        fields = 'nome_completo', 'email', 'password'

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['username'] = validated_data['email']
        usuario = Usuario.objects.create_user(**validated_data)

        return usuario

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

