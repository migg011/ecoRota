from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from EcoRota.models import Destino, Usuario

IA = 'EcoRota.viewsets.classificar_residuo'


class DescarteTestBase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='ana@exemplo.com',
            email='ana@exemplo.com',
            password='SenhaForte123',
            nome_completo='Ana Souza',
        )
        self.destino = Destino.objects.create(
            categoria='Ecoponto Centro',
            endereco='Rua das Flores, 100',
            descricao='Coleta seletiva de reciclaveis',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.usuario)

    def post_descarte(self, **overrides):
        dados = {
            'Usuario': self.usuario.id,
            'Destino': self.destino.id,
            'peso_estimado_kg': '20.00',
            'descricao_texto': 'sofa velho e quebrado',
        }
        dados.update(overrides)
        return self.client.post('/api/descartes/', dados, format='json')
