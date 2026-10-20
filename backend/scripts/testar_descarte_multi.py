import sys
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
load_dotenv(RAIZ / '.env')

import django

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from unittest.mock import patch

from django.test import Client

from EcoRota.models import Destino, Descarte, Usuario

sys.stdout.reconfigure(encoding="utf-8")

EMAIL_DEMO = "teste@ecorota.com"

CATEGORIAS_OFICIAIS = [
    "Madeira",
    "Orgânico de Estiagem",
    "Construção",
    "Secos e Recicláveis",
    "Eletroeletrônicos e Pilhas",
    "Móveis e Volumosos",
]

aprovados = 0
reprovados = 0


def verificar(nome_do_teste, condicao, detalhe):
    global aprovados, reprovados
    if condicao:
        aprovados += 1
        print(f"  [OK] {nome_do_teste} -> {detalhe}")
    else:
        reprovados += 1
        print(f"  [ERRO] {nome_do_teste} -> {detalhe}")


def main():
    print("Testando o descarte com textos de multiplos materiais")
    print("=" * 70)

    demo = Usuario.objects.filter(username=EMAIL_DEMO).first()
    verificar(
        "Usuario demo existe",
        demo is not None,
        EMAIL_DEMO if demo else "rode: python manage.py criar_usuario_demo",
    )

    destino = Destino.objects.first()
    verificar(
        "Existe pelo menos 1 destino no banco",
        destino is not None,
        "rode: python manage.py seed_destinos" if destino is None else destino.nome,
    )

    if demo is None or destino is None:
        print("=" * 70)
        print("Sem usuario ou destino nao da pra continuar")
        sys.exit(1)

    como_demo = Client(HTTP_HOST='localhost')
    como_demo.force_login(demo)

    registros_criados = []

    def postar_descarte(texto, retorno_da_ia):
        with patch(
            'EcoRota.services.classificador_ia.classificar_por_llm',
            return_value=retorno_da_ia,
        ):
            r = como_demo.post(
                '/api/descartes/',
                {
                    'Usuario': demo.id,
                    'Destino': destino.id,
                    'peso_estimado_kg': '10.00',
                    'descricao_texto': texto,
                },
                content_type='application/json',
            )
        return r

    # 1) texto com 2 materiais e IA devolvendo 2 categorias
    r = postar_descarte(
        'galhos secos e restos de tabuas de madeira',
        ['Madeira', 'Orgânico de Estiagem'],
    )
    verificar(
        "POST com 2 materiais (IA devolve lista de 2) -> 201",
        r.status_code == 201,
        f"recebido {r.status_code}",
    )
    if r.status_code == 201:
        registros_criados.append(r.json()['id'])
        categoria_gravada = r.json().get('categoria')
        verificar(
            "Categoria salva e a primeira da lista da IA",
            categoria_gravada == 'Madeira',
            f"recebido {categoria_gravada!r}",
        )

    # 2) texto com 3 materiais e IA devolvendo 3 categorias
    r = postar_descarte(
        'caixas de papelão, velhas lâmpadas e galhos de poda',
        ['Secos e Recicláveis', 'Eletroeletrônicos e Pilhas', 'Orgânico de Estiagem'],
    )
    verificar(
        "POST com 3 materiais (IA devolve lista de 3) -> 201",
        r.status_code == 201,
        f"recebido {r.status_code}",
    )
    if r.status_code == 201:
        registros_criados.append(r.json()['id'])
        categoria_gravada = r.json().get('categoria')
        verificar(
            "Categoria salva continua sendo uma oficial",
            categoria_gravada in CATEGORIAS_OFICIAIS,
            f"recebido {categoria_gravada!r}",
        )

    # 3) IA fora do ar -> fallback local por palavras-chave
    r = postar_descarte('sofá velho e quebrado', None)
    verificar(
        "POST com IA fora do ar (fallback) -> 201",
        r.status_code == 201,
        f"recebido {r.status_code}",
    )
    if r.status_code == 201:
        registros_criados.append(r.json()['id'])
        categoria_gravada = r.json().get('categoria')
        verificar(
            "Fallback gravou uma categoria oficial unica",
            categoria_gravada == 'Móveis e Volumosos',
            f"recebido {categoria_gravada!r}",
        )

    # 4) confere direto no banco que nao ficou lixo no campo
    sujos = Descarte.objects.filter(id__in=registros_criados).exclude(
        categoria__in=CATEGORIAS_OFICIAIS
    )
    verificar(
        "Nenhum registro no banco com categoria fora das 6 oficiais",
        not sujos.exists(),
        "todos limpos" if not sujos.exists() else f"{sujos.count()} com categoria suja",
    )

    # limpeza: apaga os registros de teste
    Descarte.objects.filter(id__in=registros_criados).delete()
    print(f"  [INFO] {len(registros_criados)} registro(s) de teste apagado(s)")

    print("=" * 70)
    print(f"Resultado: {aprovados} ok, {reprovados} erro(s)")

    if reprovados > 0:
        print("Algo mudou no servico - confira classificar_residuo em services/classificador_ia.py")
        sys.exit(1)
    else:
        print("Descarte com multiplos materiais funcionando como esperado!")


if __name__ == "__main__":
    main()
