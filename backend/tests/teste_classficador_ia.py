import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / '.env')

from EcoRota.services.classificador_ia import CATEGORIAS, classificar_por_llm

sys.stdout.reconfigure(encoding="utf-8")

CASOS = [
    "pallet de madeira usado",
    "resto de comida e fruta velha",
    "saco de cimento quebrado",
    "um monte de garrafa pet",
    "sofa velho e guarda-roupa quebrado",
    "tabua de madeira e saco de cimento",
    "tabuas quebradas e molhadas",
    "madeiras novinhas",
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
