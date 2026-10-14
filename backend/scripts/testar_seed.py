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

from django.db.models import Count

from EcoRota.models import Destino

sys.stdout.reconfigure(encoding="utf-8")

# Categorias oficiais do projeto (fonte unica)
CATEGORIAS_OFICIAIS = [
    "Madeira",
    "Orgânico de Estiagem",
    "Construção",
    "Secos e Recicláveis",
    "Eletroeletrônicos e Pilhas",
    "Móveis e Volumosos",
]

TOTAL_ESPERADO = 21

CONTA_ESPERADA_POR_CATEGORIA = {
    "Madeira": 2,
    "Orgânico de Estiagem": 2,
    "Construção": 2,
    "Secos e Recicláveis": 3,
    "Eletroeletrônicos e Pilhas": 10,
    "Móveis e Volumosos": 2,
}

ECOPONTOS_OFICIAIS_ESPERADOS = ["Ecoponto Zona Sul", "Ecoponto Zona Norte"]

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
    print("Testando o seed de destinos de Manaus")
    print("=" * 70)

    # 1) os campos novos do model existem?
    tem_campos_novos = hasattr(Destino, "nome") and hasattr(Destino, "horario")
    verificar(
        "Model Destino tem os campos nome e horario",
        tem_campos_novos,
        "migration 0007 aplicada" if tem_campos_novos else "rode: python manage.py migrate",
    )

    # 2) o banco tem os 21 registros?
    total = Destino.objects.count()
    verificar(
        "Total de destinos no banco",
        total == TOTAL_ESPERADO,
        f"encontrado {total}, esperado {TOTAL_ESPERADO}",
    )

    # 3) todas as categorias oficiais tem pelo menos um destino?
    categorias_no_banco = set(
        Destino.objects.values_list("categoria", flat=True).distinct()
    )
    faltando = [c for c in CATEGORIAS_OFICIAIS if c not in categorias_no_banco]
    verificar(
        "Todas as 6 categorias oficiais tem destino",
        not faltando,
        "nenhuma categoria faltando" if not faltando else f"faltando: {faltando}",
    )

    # 4) os 2 ecopontos oficiais atendem todas as categorias?
    for ecoponto in ECOPONTOS_OFICIAIS_ESPERADOS:
        qtd = Destino.objects.filter(nome=ecoponto).count()
        verificar(
            f"{ecoponto} cobre as 6 categorias",
            qtd == len(CATEGORIAS_OFICIAIS),
            f"encontrado {qtd} categorias",
        )

    # 5) a quantidade por categoria bate com o planejado?
    por_categoria = {
        i["categoria"]: i["n"]
        for i in Destino.objects.values("categoria").annotate(n=Count("id"))
    }
    for categoria, esperado in CONTA_ESPERADA_POR_CATEGORIA.items():
        encontrado = por_categoria.get(categoria, 0)
        verificar(
            f"Quantidade da categoria {categoria}",
            encontrado == esperado,
            f"encontrado {encontrado}, esperado {esperado}",
        )

    # 6) algum registro ficou com campo vazio?
    vazios = Destino.objects.filter(
        nome="" ) | Destino.objects.filter(
        endereco=""
    ) | Destino.objects.filter(descricao="") | Destino.objects.filter(horario="")
    verificar(
        "Nenhum destino com campo vazio",
        not vazios.exists(),
        "todos os campos preenchidos" if not vazios.exists() else f"{vazios.count()} com campo vazio",
    )

    # 7) existe registro duplicado de (nome, categoria)?
    duplicados = (
        Destino.objects.values("nome", "categoria")
        .annotate(n=Count("id"))
        .filter(n__gt=1)
    )
    verificar(
        "Nenhum destino duplicado",
        not duplicados.exists(),
        "sem duplicatas" if not duplicados.exists() else f"{duplicados.count()} duplicados",
    )

    print("=" * 70)
    print(f"Resultado: {aprovados} ok, {reprovados} erro(s)")

    if reprovados > 0:
        print("Dica: rode o seed de novo com: python manage.py seed_destinos")
        sys.exit(1)


if __name__ == "__main__":
    main()
