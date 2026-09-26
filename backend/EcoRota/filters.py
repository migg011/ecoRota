import django_filters

from .models import Usuario, Descarte, Destino

class UsuarioFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains'
    )

    class Meta:
        model = Usuario
        fields = ['name', 'email']

class DescarteFilter(django_filters.FilterSet):
    usuario = django_filters.CharFilter(
        field_name='usuario__id',
        lookup_expr='exact'
    )

    destino = django_filters.CharFilter(
        field_name='destino__id',
        lookup_expr='exact'
    )

    categoria = django_filters.CharFilter(
        field_name='categoria',
        lookup_expr='exact'
    )

    class Meta:
        model = Descarte
        fields = ['usuario', 'destino', 'categoria']

class DestinoFilter(django_filters.FilterSet):
    endereco = django_filters.CharFilter(
        field_name='endereco',
        lookup_expr='exact'
    )

    categoria = django_filters.CharFilter(
        field_name='categoria',
        lookup_expr='exact'
    )

    class Meta:
        model = Destino
        fields = ['endereco', 'categoria']

