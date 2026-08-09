"""A classe Catalogo. Leia o README.md antes de começar.

Esta é a peça central do projeto: carrega o JSON uma vez, constrói os
índices no __init__ e expõe os 16 métodos que o main.py e o cli.py usam.
"""
import json
from collections import deque


class Catalogo:
    def __init__(self, caminho_json: str):

        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.conteudos = dados["conteudos"]
        self.usuarios = dados["usuarios"]

        self.conteudos_por_id = {}

        for conteudo in self.conteudos:
            self.conteudos_por_id[conteudo["id"]] = conteudo

        self.usuarios_por_id = {}

        for usuario in self.usuarios:
            self.usuarios_por_id[usuario["id"]] = usuario

        self.usuarios_por_nome = {}

        for usuario in self.usuarios:
            nome = usuario["nome"].lower()
            self.usuarios_por_nome[nome] = usuario["id"]

        self.fila = deque()

    # usuários e playlists
    def listar_usuarios(self) -> list[str]:
        pass

    def buscar_usuario_por_nome(self, nome: str) -> str | None:
        pass

    def playlist_de(self, usuario_id: str) -> list[str] | None:
        pass

    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None:
        pass

    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]:
        pass

    # conteúdo
    def rating_de(self, conteudo_id: str) -> float | None:
        pass

    def duracao_total_de(self, conteudo_id: str) -> int | None:
        pass

    def generos_de(self, conteudo_id: str) -> list[str] | None:
        pass

    def plataformas_de(self, conteudo_id: str) -> list[str] | None:
        pass

    def data_adicionado_de(self, conteudo_id: str) -> str | None:
        pass

    def execucoes_de(self, conteudo_id: str) -> int | None:
        pass

    def conteudos_do_genero(self, genero: str) -> list[str]:
        pass

    # fila
    def enfileirar(self, conteudo_id: str) -> bool:
        pass

    def proximo(self) -> str | None:
        pass

    def fila_atual(self) -> list[str]:
        pass
