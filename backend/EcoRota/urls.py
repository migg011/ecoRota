from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    LoginView,
)

from .viewsets import (
    UsuarioViewSet,
    DestinoViewSet,
    DescarteViewSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'destinos', DestinoViewSet, basename='destino')
router.register(r'descartes', DescarteViewSet, basename='descarte')

urlpatterns = [
    path('auth/registro/', RegisterView.as_view(), name='api_registro'),
    path('auth/login/', LoginView.as_view(), name='api_login'),

    path('', include(router.urls)),
]