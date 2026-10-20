from EcoRota.models import Usuario
from EcoRota.tests.base import DescarteTestBase
from rest_framework import status
from rest_framework.test import APIClient


class PermissoesDestinoTests(DescarteTestBase):
    def criar_admin(self):
        return Usuario.objects.create_user(
            username='admin@exemplo.com',
            email='admin@exemplo.com',
            password='SenhaForte123',
            nome_completo='Admin Exemplo',
            is_staff=True,
        )

    def dados_de_destino(self):
        return {
            'nome': 'Ecoponto Teste',
            'categoria': 'Madeira',
            'endereco': 'Rua de Teste, 1',
            'descricao': 'Coleta de madeira',
            'horario': 'Seg a Sex, 8h as 17h',
        }

    def test_get_sem_login_retorna_401(self):
        client = APIClient()
        resposta = client.get('/api/destinos/')
        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_com_usuario_comum_retorna_200(self):
        resposta = self.client.get('/api/destinos/')
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def test_post_sem_login_retorna_401(self):
        client = APIClient()
        resposta = client.post('/api/destinos/', self.dados_de_destino(), format='json')
        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_com_usuario_comum_retorna_403(self):
        resposta = self.client.post('/api/destinos/', self.dados_de_destino(), format='json')
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_com_usuario_comum_retorna_403(self):
        resposta = self.client.put(
            f'/api/destinos/{self.destino.id}/',
            self.dados_de_destino(),
            format='json',
        )
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_com_usuario_comum_retorna_403(self):
        resposta = self.client.delete(f'/api/destinos/{self.destino.id}/')
        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_com_admin_retorna_201(self):
        admin = self.criar_admin()
        client = APIClient()
        client.force_authenticate(admin)
        resposta = client.post('/api/destinos/', self.dados_de_destino(), format='json')
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
