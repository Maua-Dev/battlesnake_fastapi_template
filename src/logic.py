# Bem-vindo ao
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# ESTE É O ARQUIVO QUE VOCÊ VAI EDITAR. Todo o resto do projeto existe
# só para levar o estado do jogo até as quatro funções abaixo.
#
# Para começar, já deixamos pronta a lógica que impede a sua cobra de andar
# para trás (ela morreria na hora). Os TODOs marcam os próximos passos.
# Documentação: https://docs.battlesnake.com

import random
import typing


# GET / — chamado quando você cadastra a cobra no site e a cada partida.
# Controla a aparência dela. Opções de cabeça, cauda e cor:
# https://docs.battlesnake.com/guides/customizations
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: coloque aqui o SEU usuário do Battlesnake
        "color": "#8B0000",  # TODO: escolha a cor da sua cobra
        "head": "tiger-king",  # TODO: escolha a cabeça
        "tail": "hook",  # TODO: escolha a cauda
        "version": "1.0.0",
    }


# POST /start — chamado uma vez, quando a partida começa.
# Bom lugar para preparar qualquer estado inicial.
def start(game_state: typing.Dict) -> None:
    print(f"JOGO COMEÇOU (partida {game_state['game']['id']})")


# POST /end — chamado uma vez, quando a partida termina.
def end(game_state: typing.Dict) -> None:
    print(f"FIM DE JOGO após {game_state['turn']} turnos")


# POST /move — chamado a cada turno. Aqui mora a inteligência da sua cobra.
# Precisa devolver "up", "down", "left" ou "right".
# Exemplo do JSON recebido: https://docs.battlesnake.com/api/example-move
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # --- Impedir que a cobra ande para trás (já implementado) ---
    # O pescoço é a parte do corpo logo atrás da cabeça. Voltar por cima dele
    # é morte certa, então marcamos aquela direção como insegura.
    my_head = game_state["you"]["body"][0]  # coordenadas da sua cabeça
    my_neck = game_state["you"]["body"][1]  # coordenadas do seu "pescoço"

    if my_neck["x"] < my_head["x"]:
        # pescoço à esquerda da cabeça -> não vá para a esquerda
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:
        # pescoço à direita da cabeça -> não vá para a direita
        is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:
        # pescoço abaixo da cabeça -> não desça
        is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:
        # pescoço acima da cabeça -> não suba
        is_move_safe["up"] = False

    # TODO: Passo 1 - impedir que a cobra saia do tabuleiro
    # board_width = game_state["board"]["width"]
    # board_height = game_state["board"]["height"]

    # TODO: Passo 2 - impedir que a cobra bata no próprio corpo
    # my_body = game_state["you"]["body"]

    # TODO: Passo 3 - impedir que a cobra bata nas adversárias
    # opponents = game_state["board"]["snakes"]

    # Sobrou alguma direção segura?
    safe_moves = [direction for direction, is_safe in is_move_safe.items() if is_safe]

    if not safe_moves:
        print(f"MOVE {game_state['turn']}: sem saída! descendo")
        return {"move": "down"}

    # Escolhe uma direção segura ao acaso.
    next_move = random.choice(safe_moves)

    # TODO: Passo 4 - ir atrás da comida em vez de sortear, para não morrer de fome
    # food = game_state["board"]["food"]

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}
