from django.core.management.base import BaseCommand

from EcoRota.models import Destino


# Categorias oficiais do projeto (fonte unica)
CATEGORIAS = [
    "Madeira",
    "Orgânico de Estiagem",
    "Construção",
    "Secos e Recicláveis",
    "Eletroeletrônicos e Pilhas",
    "Móveis e Volumosos",
]

HORARIO_PADRAO = "Seg a Sáb, 8h às 18h - confirme no Manaus Atende (156)"

# Fontes: Portal Tambaqui (02/2026), Green Eletron e Prefeitura de Manaus
LOCAIS = [
    # Ecopontos oficiais da Prefeitura atendem todas as categorias
    {
        "nome": "Ecoponto Zona Sul",
        "endereco": "Avenida Lourenço da Silva Braga, 1403-1409 - Educandos",
        "descricao": (
            "Ecoponto oficial da Prefeitura de Manaus. "
            "Aceita eletrônicos, eletrodomésticos, pilhas, baterias e cabos."
        ),
        "horario": HORARIO_PADRAO,
        "categorias": CATEGORIAS,
    },
    {
        "nome": "Ecoponto Zona Norte",
        "endereco": "Parque dos Bilhares - Zona Norte",
        "descricao": (
            "Ecoponto oficial da Prefeitura de Manaus. "
            "Confirmar endereço exato pelo Manaus Atende (156)."
        ),
        "horario": HORARIO_PADRAO,
        "categorias": CATEGORIAS,
    },
    # PEVs parceiros (Green Eletron) aceitam apenas eletroeletrônicos e pilhas
    {
        "nome": "PEV Amazonas Shopping",
        "endereco": "Avenida Djalma Batista, 482 - Parque 10 de Novembro",
        "descricao": "Ponto de entrega voluntária de eletroeletrônico dentro do shopping.",
        "horario": HORARIO_PADRAO,
        "categorias": ["Eletroeletrônicos e Pilhas"],
    },
    {
        "nome": "PEV Manauara Shopping",
        "endereco": "Avenida Mário Ypiranga, 1300 - Adrianópolis",
        "descricao": "Ponto de entrega voluntária de eletroeletrônico dentro do shopping.",
        "horario": HORARIO_PADRAO,
        "categorias": ["Eletroeletrônicos e Pilhas"],
    },
    {
        "nome": "PEV Shopping Grande Circular",
        "endereco": "Avenida Autaz Mirim, 6100 - São José Operário",
        "descricao": "Ponto de entrega voluntária de eletroeletrônico dentro do shopping.",
        "horario": HORARIO_PADRAO,
        "categorias": ["Eletroeletrônicos e Pilhas"],
    },
    {
        "nome": "PEV Shopping Ponta Negra",
        "endereco": "Avenida Coronel Teixeira, 5705 - Compensa",
        "descricao": "Ponto de entrega voluntária de eletroeletrônico dentro do shopping.",
        "horario": HORARIO_PADRAO,
        "categorias": ["Eletroeletrônicos e Pilhas"],
    },
    {
        "nome": "PEV Studio 5 Shopping",
        "endereco": "Avenida Rodrigo Otávio, 3555 - Japiim",
        "descricao": "Ponto de entrega voluntária de eletroeletrônico dentro do shopping.",
        "horario": HORARIO_PADRAO,
        "categorias": ["Eletroeletrônicos e Pilhas"],
    },
    {
        "nome": "PEV Sumauma Shopping",
        "endereco": "Avenida Noel Nutels, 1762 - Cidade Nova",
        "descricao": "Ponto de entrega voluntária de eletroeletrônico dentro do shopping.",
        "horario": HORARIO_PADRAO,
        "categorias": ["Eletroeletrônicos e Pilhas"],
    },
    {
        "nome": "PEV Bemol Matriz",
        "endereco": "Rua Miranda Leão, 41 - Centro",
        "descricao": "Ponto de entrega voluntária de eletroeletrônico na loja Bemol.",
        "horario": HORARIO_PADRAO,
        "categorias": ["Eletroeletrônicos e Pilhas"],
    },
    {
        "nome": "PEV Bemol Torquato",
        "endereco": "Avenida Torquato Tapajós, 8253 - Tarumã",
        "descricao": "Ponto de entrega voluntária de eletroeletrônico na loja Bemol.",
        "horario": HORARIO_PADRAO,
        "categorias": ["Eletroeletrônicos e Pilhas"],
    },
    # Cooperativa de catadores recebe recicláveis secos
    {
        "nome": "Ascarman - Santa Etelvina",
        "endereco": "Rua Helena Cardoso, S/N - Santa Etelvina",
        "descricao": (
            "Associação de catadores de recicláveis do Amazonas. "
            "Coleta agendada pelo telefone (92) 99342-8866."
        ),
        "horario": "Consulte pelo telefone (92) 99342-8866",
        "categorias": ["Secos e Recicláveis"],
    },
]


class Command(BaseCommand):
    help = "Popula a tabela de destinos com ecopontos e pontos de coleta reais de Manaus"

    def handle(self, *args, **options):
        criados = 0

        for local in LOCAIS:
            for categoria in local["categorias"]:
                Destino.objects.update_or_create(
                    nome=local["nome"],
                    categoria=categoria,
                    defaults={
                        "endereco": local["endereco"],
                        "descricao": local["descricao"],
                        "horario": local["horario"],
                    },
                )
                criados += 1

        self.stdout.write(self.style.SUCCESS(f"Destinos populados: {criados}"))
