from unittest.mock import patch

from EcoRota.tests.base import DescarteTestBase
from rest_framework import status
from rest_framework.test import APIClient

# a view importa a funcao direto, entao o mock tem que ser aplicado no nome dela
API = 'EcoRota.views.classificar_residuo'


class ClassificarApiTests(DescarteTestBase):
    def post_classificar(self, **overrides):
        dados = {
            'descricao_texto': 'sofa velho e quebrado',
        }
        dados.update(overrides)
        return self.client.post('/api/classificar/', dados, format='json')

    def test_classificar_devolve_200_com_categoria_e_destinos(self):
        with patch(API, return_value='Móveis e Volumosos'):
            resposta = self.post_classificar()
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data['categoria'], 'Móveis e Volumosos')
        self.assertIn('destinos', resposta.data)

    def test_destinos_vem_filtrados_somente_pela_categoria(self):
        with patch(API, return_value='Móveis e Volumosos'):
            resposta = self.post_classificar()
        for destino in resposta.data['destinos']:
            self.assertEqual(destino['categoria'], 'Móveis e Volumosos')

    def test_destinos_incluem_os_campos_do_ecoponto(self):
        with patch(API, return_value='Móveis e Volumosos'):
            resposta = self.post_classificar()
        if resposta.data['destinos']:
            destino = resposta.data['destinos'][0]
            self.assertIn('nome', destino)
            self.assertIn('horario', destino)
            self.assertIn('endereco', destino)

    def test_texto_com_menos_de_tres_caracteres_e_rejeitado(self):
        resposta = self.post_classificar(descricao_texto='ab')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('descricao_texto', resposta.data)

    def test_sem_login_da_401(self):
        client = APIClient()
        resposta = client.post(
            '/api/classificar/',
            {'descricao_texto': 'sofa velho'},
            format='json',
        )
        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_resposta_de_lista_de_categorias_usa_a_primeira(self):
        with patch(API, return_value=['Madeira', 'Construção']):
            resposta = self.post_classificar(descricao_texto='tábua com prego')
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data['categoria'], 'Madeira')
