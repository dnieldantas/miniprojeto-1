from catalogo import Catalogo
import sys


def ler_inteiro(mensagem):
    # nunca deixa o int() quebrar o menu
    valor = input(mensagem)

    if not valor.isdigit():
        print("Digite um numero valido.")
        return None

    return int(valor)


def menu(catalogo):
    while True:
        print("""
=== TrilhaSonora ===

1. Listar todos os usuários
2. Ver playlist completa de um usuário
3. Conteúdo na posição N da playlist
4. Interseção de playlists (N usuários)
5. Dados de um conteúdo
6. Conteúdos de um gênero
7. Enfileirar conteúdo na fila de reprodução
8. Tocar próximo da fila
9. Ver fila atual
0. Sair
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            usuarios = catalogo.listar_usuarios()

            print("Usuários:")

            for usuario in usuarios:
                print(usuario)

        elif opcao == "2":
            nome = input("Nome do usuário: ")

            usuario_id = catalogo.buscar_usuario_por_nome(nome)

            if usuario_id is None:
                print("Usuário não encontrado.")
                continue

            playlist = catalogo.playlist_de(usuario_id)

            print(f"Playlist de {nome} ({len(playlist)} itens):")

            for i, conteudo_id in enumerate(playlist, start=1):
                print(f"{i}. {catalogo.descrever(conteudo_id)}")

        elif opcao == "3":
            nome = input("Nome do usuário: ")

            usuario_id = catalogo.buscar_usuario_por_nome(nome)

            if usuario_id is None:
                print("Usuário não encontrado.")
                continue

            playlist = catalogo.playlist_de(usuario_id)

            print(f"Playlist de {nome} tem {len(playlist)} itens (posições 1 a {len(playlist)}).")

            posicao = ler_inteiro("Posição: ")

            if posicao is None:
                continue

            # conversao de 1-based (humano) pra 0-based (contrato da Catalogo)
            conteudo_id = catalogo.conteudo_na_posicao(usuario_id, posicao - 1)

            if conteudo_id is None:
                print("Posição inválida.")
                continue

            print(catalogo.descrever(conteudo_id))

        elif opcao == "4":
            quantidade = ler_inteiro("Quantidade de usuários: ")

            if quantidade is None:
                continue

            usuario_ids = []

            for i in range(quantidade):
                nome = input("Nome do usuário: ")

                usuario_id = catalogo.buscar_usuario_por_nome(nome)

                if usuario_id is None:
                    print("Usuário não encontrado.")
                    usuario_ids = []
                    break

                usuario_ids.append(usuario_id)

            if len(usuario_ids) == 0:
                continue

            resultado = catalogo.intersecao_playlists(usuario_ids)

            if len(resultado) == 0:
                print("Nenhum conteúdo em comum.")
                continue

            print("Conteúdos em comum:")

            for conteudo_id in resultado:
                print(catalogo.descrever(conteudo_id))

        elif opcao == "5":
            conteudo_id = input("ID do conteúdo: ")

            if conteudo_id not in catalogo.conteudos_por_id:
                print("Conteúdo não encontrado.")
                continue

            rating = catalogo.rating_de(conteudo_id)
            duracao = catalogo.duracao_total_de(conteudo_id)
            generos = catalogo.generos_de(conteudo_id)
            plataformas = catalogo.plataformas_de(conteudo_id)
            data = catalogo.data_adicionado_de(conteudo_id)

            print(f"""
{catalogo.descrever(conteudo_id)}
Rating: {rating}
Duração: {duracao} segundos
Gêneros: {generos}
Plataformas: {plataformas}
Data de adição: {data}
""")

            conteudo = catalogo.conteudos_por_id[conteudo_id]

            if conteudo["tipo"] == "musica":
                execucoes = catalogo.execucoes_de(conteudo_id)
                print(f"Execuções: {execucoes}")

        elif opcao == "6":
            genero = input("Gênero: ")

            resultado = catalogo.conteudos_do_genero(genero)

            if len(resultado) == 0:
                print("Nenhum conteúdo nesse gênero.")
                continue

            print("Conteúdos:")

            for conteudo_id in resultado:
                print(catalogo.descrever(conteudo_id))

        elif opcao == "7":
            conteudo_id = input("ID do conteúdo: ")

            sucesso = catalogo.enfileirar(conteudo_id)

            if sucesso:
                print(f"Enfileirado: {catalogo.descrever(conteudo_id)}")
            else:
                print("Conteúdo não encontrado.")

        elif opcao == "8":
            conteudo_id = catalogo.proximo()

            if conteudo_id is None:
                print("A fila está vazia.")
            else:
                print(f"Reproduzindo: {catalogo.descrever(conteudo_id)}")

        elif opcao == "9":
            fila = catalogo.fila_atual()

            if len(fila) == 0:
                print("Fila vazia.")
                continue

            print("Fila atual:")

            for i, conteudo_id in enumerate(fila, start=1):
                print(f"{i}. {catalogo.descrever(conteudo_id)}")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


def main():
    if len(sys.argv) != 2:
        print("Uso: python cli.py catalogo_final.json")
        return

    caminho_json = sys.argv[1]

    catalogo = Catalogo(caminho_json)

    menu(catalogo)


if __name__ == "__main__":
    main()