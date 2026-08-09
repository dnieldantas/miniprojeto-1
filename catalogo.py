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
        nomes = []

        for usuario in self.usuarios:
            nomes.append(usuario["nome"])

        nomes.sort()

        return nomes

    def buscar_usuario_por_nome(self, nome: str) -> str | None:
        nome = nome.lower()

        if nome in self.usuarios_por_nome:
            return self.usuarios_por_nome[nome]

        return None

    def playlist_de(self, usuario_id: str) -> list[str] | None:
        if usuario_id in self.usuarios_por_id:
            usuario = self.usuarios_por_id[usuario_id]
            return usuario["playlist"]

        return None

    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None:
        playlist = self.playlist_de(usuario_id)

        if playlist is None:
            return None

        if posicao < 0 or posicao >= len(playlist):
            return None

        return playlist[posicao]

    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]:
        playlists = []

        for usuario_id in usuario_ids:
            playlist = self.playlist_de(usuario_id)

            if playlist is None:
                return []

            playlists.append(playlist)

        if len(playlists) == 0:
            return []

        intersecao = set(playlists[0])

        for i in range(1, len(playlists)):
            intersecao = intersecao & set(playlists[i])

        resultado = list(intersecao)
        resultado.sort()

        return resultado

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
