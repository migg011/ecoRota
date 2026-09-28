import os
import logging
from groq import Groq, GroqError

logger = logging.getLogger(__name__)

CATEGORIAS = [
    "Madeira",
    "Orgânico de Estiagem",
    "Construção",
    "Recicláveis",
    "Eletrónicos",
    "Móveis",
]

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY não configurada")
        _client = Groq(api_key=api_key)
    return _client


def classificar_por_llm(texto: str) -> list[str] | None:
    try:
        client = _get_client()
        resposta = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": (
                    f"Classifique o resíduo descrito em EXATAMENTE uma destas categorias. Em caso de mais de um material dentro da descrição, pule uma linha e escreva a categoria correta individualmente: "
                    f"{', '.join(CATEGORIAS)}.\n"
                    f"Responda APENAS com o nome exato da categoria, sem explicação.\n"
                    f"Resíduo: {texto}"

                )
            }]
        )
        categoria_bruta = resposta.choices[0].message.content.strip()

        achadas = []
        for linha in categoria_bruta.splitlines():
            for categoria in CATEGORIAS:
                if categoria.lower() in linha.lower():
                    achadas.append(categoria)

        if not achadas:
            logger.warning(f"LLM retornou categoria não reconhecida: {categoria_bruta}")
            return None

        return achadas

    except GroqError:
        logger.exception("Falha na chamada: API da Groq")
        return None


def classificar_por_palavras_chave(texto: str) -> str:
    texto_lower = texto.lower()

    mots_madeira = [
        "madeira",
        "tabua",
        "tábua",
        "palete",
        "pallet",
        "compensado",
        "ripa"
    ]

    mots_organico = [
        "folha",
        "galho",
        "poda",
        "tronco",
        "grama",
        "arvore",
        "árvore",
        "vegetação",
        "cinza",
        "queimada",
    ]

    mots_construcao = [
        "tijolo",
        "gesso",
        "entulho",
        "concreto",
        "cimento",
        "piso",
        "azulejo",
        "pedra",
        "areia",
        "brita",
    ]

    mots_reciclaveis = [
        "plastico",
        "plástico",
        "garrafa",
        "papel",
        "papelao",
        "papelão",
        "caixa",
        "lata",
        "metal",
        "vidro"
    ]

    mots_eletronicos = [
        "computador",
        "tv",
        "televisao",
        "televisão",
        "fio",
        "cabo",
        "bateria",
        "pilha",
        "celular",
        "eletro"]

    mots_moveis = [
        "sofa",
        "sofá",
        "colchão",
        "colchao",
        "armario",
        "armário",
        "mesa",
        "cadeira",
        "estante"
    ]

    if any(p in texto_lower for p in mots_madeira):
        return "Madeira"
    if any(p in texto_lower for p in mots_organico):
        return "Orgânico de Estiagem"
    if any(p in texto_lower for p in mots_construcao):
        return "Construção"
    if any(p in texto_lower for p in mots_reciclaveis):
        return "Secos e Recicláveis"
    if any(p in texto_lower for p in mots_eletronicos):
        return "Eletroeletrônicos e Pilhas"
    if any(p in texto_lower for p in mots_moveis):
        return "Móveis e Volumosos"

    #padrao
    return "Construção"


def classificar_residuo(texto: str) -> str:
    categoria = classificar_por_llm(texto)

    if categoria is not None:
        return categoria

    logger.info(f"Executando fallback local por palavras-chave para o texto: '{texto}'")
    return classificar_por_palavras_chave(texto)
