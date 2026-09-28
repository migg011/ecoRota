from django.test import SimpleTestCase

from EcoRota.services.classificador_ia import classificar_por_palavras_chave


class ClassificadorFallbackTests(SimpleTestCase):
    def test_classifica_por_palavra_chave(self):
        casos = {
            'pallet de madeira usado': 'Madeira',
            'saco de cimento quebrado': 'Construção',
            'garrafa pet vazia': 'Secos e Recicláveis',
            'bateria de celular velha': 'Eletroeletrônicos e Pilhas',
        }
        for texto, esperado in casos.items():
            with self.subTest(texto=texto):
                self.assertEqual(classificar_por_palavras_chave(texto), esperado)

    def test_texto_sem_palavra_conhecida_cai_no_padrao(self):
        self.assertEqual(classificar_por_palavras_chave('xyzzy'), 'Construção')
