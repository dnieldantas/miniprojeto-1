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
        if conteudo_id not in self.conteudos_por_id:
            return None

        conteudo = self.conteudos_por_id[conteudo_id]

        if "rating" not in conteudo:
            return None

        return float(conteudo["rating"])

    def duracao_total_de(self, conteudo_id: str) -> int | None:
        if conteudo_id not in self.conteudos_por_id:
            return None

        conteudo = self.conteudos_por_id[conteudo_id]

        if conteudo["tipo"] == "musica":
            if "duracao_seg" not in conteudo:
                return None

            return conteudo["duracao_seg"]

        if conteudo["tipo"] == "album":
            if "faixas" not in conteudo:
                return None

            total_segundos = 0

            for faixa in conteudo["faixas"]:
                if faixa["duracao_seg"] is not None:
                    total_segundos += faixa["duracao_seg"]

            return total_segundos

        return None

    def generos_de(self, conteudo_id: str) -> list[str] | None:
        if conteudo_id not in self.conteudos_por_id:
            return None

        conteudo = self.conteudos_por_id[conteudo_id]

        if "generos" not in conteudo:
            return []

        generos = []

        def adicionar_generos(valor):
            if isinstance(valor, str):
                generos.append(valor)
                return

            for item in valor:
                adicionar_generos(item)

        adicionar_generos(conteudo["generos"])

        generos.sort()

        return generos

    def plataformas_de(self, conteudo_id: str) -> list[str] | None:
        if conteudo_id not in self.conteudos_por_id:
            return None

        conteudo = self.conteudos_por_id[conteudo_id]

        if "plataformas" not in conteudo:
            return []

        plataformas = []

        for plataforma in conteudo["plataformas"]:
            plataformas.append(plataforma)

        plataformas.sort()

        return plataformas

    def data_adicionado_de(self, conteudo_id: str) -> str | None:
        if conteudo_id not in self.conteudos_por_id:
            return None

        conteudo = self.conteudos_por_id[conteudo_id]

        if "data_adicionado" not in conteudo:
            return None

        data = conteudo["data_adicionado"]

        if "/" in data:
            partes = data.split("/")

            dia = partes[0]
            mes = partes[1]
            ano = partes[2]

            return ano + "-" + mes + "-" + dia

        return data

    def execucoes_de(self, conteudo_id: str) -> int | None:
        if conteudo_id not in self.conteudos_por_id:
            return None

        conteudo = self.conteudos_por_id[conteudo_id]

        if conteudo["tipo"] != "musica":
            return None

        if "engajamento" not in conteudo:
            return None

        if "execucoes" not in conteudo["engajamento"]:
            return None

        execucoes = conteudo["engajamento"]["execucoes"]

        if isinstance(execucoes, str):
            execucoes = execucoes.replace(",", "")

        return int(execucoes)

    def conteudos_do_genero(self, genero: str) -> list[str]:
        resultado = []

        for conteudo in self.conteudos:
            generos = self.generos_de(conteudo["id"])

            if generos is None:
                continue

            for genero_conteudo in generos:
                if genero_conteudo == genero:
                    resultado.append(conteudo["id"])
                    break

        resultado.sort()

        return resultado

    def descrever(self, conteudo_id: str) -> str:
        if conteudo_id not in self.conteudos_por_id:
            return f"[conteudo {conteudo_id} nao encontrado]"

        conteudo = self.conteudos_por_id[conteudo_id]

        return f"{conteudo['titulo']}, de {conteudo['artista']} ({conteudo['tipo']})"

    # fila
    def enfileirar(self, conteudo_id: str) -> bool:
        if conteudo_id not in self.conteudos_por_id:
            return False

        self.fila.append(conteudo_id)

        return True

    def proximo(self) -> str | None:
        if len(self.fila) == 0:
            return None

        return self.fila.popleft()

    def fila_atual(self) -> list[str]:
        resultado = []

        for conteudo_id in self.fila:
            resultado.append(conteudo_id)

        return resultado