from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Usuario, Destino, Descarte
from .serializers import UsuarioSerializer, DestinoSerializer, DescarteSerializer
from .filters import DestinoFilter, DescarteFilter, UsuarioFilter
from .services.classificador_ia import classificar_residuo


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filterset_class = UsuarioFilter
    ordering_fields = ('nome', 'email')

class DestinoViewSet(viewsets.ModelViewSet):
    queryset = Destino.objects.all()
    serializer_class = DestinoSerializer
    filterset_class = DestinoFilter
    ordering_fields = ('endereco', 'categoria')

class DescarteViewSet(viewsets.ModelViewSet):
    queryset = Descarte.objects.all()
    serializer_class = DescarteSerializer
    filterset_class = DescarteFilter
    ordering_fields = ('usuario__id','destino__id', 'categoria')

    def perform_create(self, serializer):
        descricao = serializer.validated_data['input_do_usuario']
        categoria_identificada = classificar_residuo(descricao)
        serializer.save(categoria=categoria_identificada)
