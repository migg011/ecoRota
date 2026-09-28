from decimal import Decimal
from unittest.mock import patch

from EcoRota.models import Descarte
from EcoRota.serializers import DescarteSerializer
from EcoRota.tests.base import IA, DescarteTestBase
from rest_framework import status


class DataCriacaoTests(DescarteTestBase):
    def test_cliente_nao_preenche_data_criacao(self):
        with patch(IA, return_value='Móveis'):
            resposta = self.post_descarte()
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Descarte.objects.get().data_criacao)

    def test_data_criacao_enviada_pelo_cliente_e_descartada(self):
        with patch(IA, return_value='Móveis'):
            resposta = self.post_descarte(data_criacao='1999-01-01T00:00:00Z')
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertGreater(Descarte.objects.get().data_criacao.year, 2000)

    def test_data_criacao_e_read_only_no_serializer(self):
        self.assertTrue(DescarteSerializer().fields['data_criacao'].read_only)

    def test_data_criacao_e_imutavel_em_update(self):
        with patch(IA, return_value='Móveis'):
            self.post_descarte()
        descarte = Descarte.objects.get()
        original = descarte.data_criacao
        descarte.categoria = 'Construção'
        descarte.save()
        descarte.refresh_from_db()
        self.assertEqual(descarte.data_criacao, original)


class PesoEstimadoTests(DescarteTestBase):
    def test_peso_negativo_e_rejeitado(self):
        with patch(IA, return_value='Móveis'):
            resposta = self.post_descarte(peso_estimado_kg='-50.00')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('peso_estimado_kg', resposta.data)

    def test_peso_com_excesso_de_digitos_e_rejeitado(self):
        with patch(IA, return_value='Móveis'):
            resposta = self.post_descarte(peso_estimado_kg='999999999.00')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('peso_estimado_kg', resposta.data)

    def test_peso_e_gravado_com_duas_casas_decimais(self):
        with patch(IA, return_value='Móveis'):
            self.post_descarte(peso_estimado_kg='20.50')
        self.assertEqual(Descarte.objects.get().peso_estimado_kg, Decimal('20.50'))

    def test_dois_descartes_com_o_mesmo_peso_sao_aceitos(self):
        with patch(IA, return_value='Móveis'):
            primeira = self.post_descarte()
            segunda = self.post_descarte()
        self.assertEqual(primeira.status_code, status.HTTP_201_CREATED)
        self.assertEqual(segunda.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Descarte.objects.count(), 2)

    def test_o_model_aceita_peso_repetido(self):
        Descarte.objects.create(Usuario=self.usuario, Destino=self.destino,
                                peso_estimado_kg=Decimal('20.00'), categoria='Móveis',
                                input_do_usuario='sofa velho')
        Descarte.objects.create(Usuario=self.usuario, Destino=self.destino,
                                peso_estimado_kg=Decimal('20.00'), categoria='Móveis',
                                input_do_usuario='sofa velho')
        self.assertEqual(Descarte.objects.count(), 2)


class DescricaoTextoTests(DescarteTestBase):
    def test_texto_recebido_chega_intato_ao_classificador(self):
        with patch(IA, return_value='Móveis') as classificador:
            self.post_descarte(descricao_texto='tábua de madeira molhada')
        classificador.assert_called_once_with('tábua de madeira molhada')

    def test_texto_e_gravado_na_coluna_input_do_usuario(self):
        with patch(IA, return_value='Móveis'):
            self.post_descarte(descricao_texto='garrafa pet vazia')
        self.assertEqual(Descarte.objects.get().input_do_usuario, 'garrafa pet vazia')

    def test_resposta_devolve_descricao_texto_e_nao_input_do_usuario(self):
        with patch(IA, return_value='Móveis'):
            resposta = self.post_descarte()
        self.assertNotIn('input_do_usuario', resposta.data)
        self.assertEqual(resposta.data['descricao_texto'], 'sofa velho e quebrado')

    def test_texto_com_menos_de_tres_caracteres_e_rejeitado(self):
        with patch(IA, return_value='Móveis'):
            resposta = self.post_descarte(descricao_texto='ab')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('descricao_texto', resposta.data)

    def test_texto_vazio_e_rejeitado(self):
        with patch(IA, return_value='Móveis'):
            resposta = self.post_descarte(descricao_texto='')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dois_descartes_com_o_mesmo_texto_sao_aceitos(self):
        with patch(IA, return_value='Móveis'):
            primeira = self.post_descarte()
            segunda = self.post_descarte()
        self.assertEqual(primeira.status_code, status.HTTP_201_CREATED)
        self.assertEqual(segunda.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Descarte.objects.count(), 2)


class CategoriaTests(DescarteTestBase):
    def test_categoria_e_read_only_no_serializer(self):
        self.assertTrue(DescarteSerializer().fields['categoria'].read_only)

    def test_categoria_enviada_pelo_cliente_e_descartada(self):
        with patch(IA, return_value='Construção'):
            self.post_descarte(categoria='Categoria Injetada')
        self.assertEqual(Descarte.objects.get().categoria, 'Construção')

    def test_cliente_nao_informa_categoria_e_o_create_ainda_funciona(self):
        with patch(IA, return_value='Móveis') as classificador:
            resposta = self.post_descarte()
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        classificador.assert_called_once()
