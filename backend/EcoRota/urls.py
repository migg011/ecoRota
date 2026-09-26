from rest_framework.routers import DefaultRouter

from .viewsets import UsuarioViewSet, DestinoViewSet, DescarteViewSet

router = DefaultRouter()

router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'descartes', DescarteViewSet, basename='descarte')
router.register(r'destinos', DestinoViewSet, basename='destino')

urlpatterns = router.urls