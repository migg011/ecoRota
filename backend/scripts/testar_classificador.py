import sys
import time
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
load_dotenv(RAIZ / '.env')

from EcoRota.services.classificador_ia import CATEGORIAS, classificar_por_llm

sys.stdout.reconfigure(encoding="utf-8")

CASOS = [
    "pedra",
    "prego",
    "madeira velha",
]


def main():
    print("categorias:", CATEGORIAS)
    print("-" * 70)
    for texto in CASOS:
        inicio = time.perf_counter()
        resultado = classificar_por_llm(texto)
        decorrido = time.perf_counter() - inicio
        print(f"{texto!r:42} -> {resultado!r:26} {decorrido:.1f}s")


if __name__ == "__main__":
    main()
