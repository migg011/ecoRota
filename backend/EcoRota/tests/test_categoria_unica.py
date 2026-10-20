from unittest import TestCase
from unittest.mock import patch

from EcoRota.services.classificador_ia import CATEGORIAS, classificar_residuo
from EcoRota.tests.base import DescarteTestBase
from rest_framework import status

# o mock tem que ser aplicado no nome da funcao dentro do modulo do servico
LLM = 'EcoRota.services.classificador_ia.classificar_por_llm'


class CategoriaUnicaTests(TestCase):
    def test_lista_da_ia_vira_somente_a_primeira(self):
        with patch(LLM, return_value=['Madeira', 'Orgânico de Estiagem']):
            categoria = classificar_residuo('galhos secos e restos de tabuas de madeira')
        self.assertEqual(categoria, 'Madeira')

    def test_lista_com_uma_categoria_devolve_elas_mesma(self):
        with patch(LLM, return_value=['Móveis e Volumosos']):
            categoria = classificar_residuo('sofa velho')
        self.assertEqual(categoria, 'Móveis e Volumosos')

    def test_ia_falhando_usa_o_fallback_de_uma_categoria(self):
        with patch(LLM, return_value=None):
            categoria = classificar_residuo('sofá velho e quebrado')
        self.assertEqual(categoria, 'Móveis e Volumosos')

    def test_resultado_sempre_e_uma_das_categorias_oficiais(self):
        with patch(LLM, return_value=['Secos e Recicláveis', 'Construção']):
            categoria = classificar_residuo('papelão e entulho')
        self.assertIn(categoria, CATEGORIAS)


class DescarteComTextoMultiplTests(DescarteTestBase):
    def post_com_ia_de_lista(self):
        with patch(LLM, return_value=['Madeira', 'Orgânico de Estiagem']):
            return self.post_descarte(descricao_texto='galhos secos e restos de tabuas')

    def test_post_com_texto_multi_devolve_201(self):
        resposta = self.post_com_ia_de_lista()
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

    def test_post_com_texto_multi_grava_uma_categoria_oficial(self):
        resposta = self.post_com_ia_de_lista()
        self.assertEqual(resposta.data['categoria'], 'Madeira')
        self.assertIn(resposta.data['categoria'], CATEGORIAS)

    def test_post_com_texto_multi_grava_categoria_limpa_no_banco(self):
        self.post_com_ia_de_lista()
        from EcoRota.models import Descarte
        registro = Descarte.objects.latest('id')
        self.assertEqual(registro.categoria, 'Madeira')
