"""Modo batch: lê consultas.json, responde em ordem, grava respostas.json.

Uso: python main.py consultas.json respostas.json
"""

import json
import sys
from catalogo import Catalogo


def main():
    caminho_consultas = sys.argv[1]
    caminho_respostas = sys.argv[2]

    catalogo = Catalogo("catalogo_final.json")

    with open(caminho_consultas, "r", encoding="utf-8") as f:
        dados_consultas = json.load(f)

    respostas = {}

    for consulta in dados_consultas["consultas"]:
        id_consulta = consulta["id"]
        tipo = consulta["tipo"]
        parametros = consulta["parametros"]

        metodo = getattr(catalogo, tipo)
        resultado = metodo(**parametros)

        respostas[str(id_consulta)] = resultado

    with open(caminho_respostas, "w", encoding="utf-8") as f:
        json.dump(respostas, f, ensure_ascii=False, indent=2)

    print(f"{len(respostas)} respostas gravadas em {caminho_respostas}")


if __name__ == "__main__":
    main()