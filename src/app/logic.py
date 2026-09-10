# Bem-vindo ao
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \   __\   __\  | _/ __ \ /  ___//    \__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\_____>
#
# ESTE É O ARQUIVO QUE VOCÊ VAI EDITAR. Todo o resto do projeto existe
# só para levar o estado do jogo até as quatro funções abaixo.
#
# Para começar, já deixamos pronta a lógica que impede a sua cobra de andar
# para trás (ela morreria na hora). Os TODOs marcam os próximos passos.
# Documentação: https://docs.battlesnake.com

import random
import logging
from .models import GameState, MoveResponse

logger = logging.getLogger(__name__)


def info() -> dict:
    """GET / — chamado quando você cadastra a cobra e a cada partida.
    Controla a aparência dela.
    Opções de cabeça, cauda e cor: https://docs.battlesnake.com/guides/customizations
    """
    logger.info("INFO")

    return {
        "apiversion": "1",
        "author": "",          # TODO: coloque aqui o SEU usuário do Battlesnake
        "color": "#8B0000",    # TODO: escolha a cor da sua cobra
        "head": "tiger-king",  # TODO: escolha a cabeça
        "tail": "hook",        # TODO: escolha a cauda
        "version": "1.0.0",
    }


def start(state: GameState) -> None:
    """POST /start — chamado uma vez, quando a partida começa.
    Bom lugar para preparar qualquer estado inicial.
    """
    logger.info("JOGO COMEÇOU (partida %s)", state.game.id)


def end(state: GameState) -> None:
    """POST /end — chamado uma vez, quando a partida termina."""
    logger.info("FIM DE JOGO após %d turnos", state.turn)


def get_move(state: GameState) -> MoveResponse:
    """POST /move — chamado a cada turno. Aqui mora a inteligência da sua cobra.
    Precisa devolver "up", "down", "left" ou "right".
    Exemplo do JSON recebido: https://docs.battlesnake.com/api/example-move
    """
    is_move_safe: dict[str, bool] = {
        "up": True,
        "down": True,
        "left": True,
        "right": True,
    }

    # --- Impedir que a cobra ande para trás (já implementado) ---
    # O pescoço é a parte do corpo logo atrás da cabeça. Voltar por cima dele
    # é morte certa, então marcamos aquela direção como insegura.
    my_head = state.you.body[0]
    my_neck = state.you.body[1] if len(state.you.body) >= 2 else None

    if my_neck is not None:
        if my_neck.x < my_head.x:
            # pescoço à esquerda da cabeça -> não vá para a esquerda
            is_move_safe["left"] = False
        elif my_neck.x > my_head.x:
            # pescoço à direita da cabeça -> não vá para a direita
            is_move_safe["right"] = False
        elif my_neck.y < my_head.y:
            # pescoço abaixo da cabeça -> não desça
            is_move_safe["down"] = False
        elif my_neck.y > my_head.y:
            # pescoço acima da cabeça -> não suba
            is_move_safe["up"] = False

    # TODO: Passo 1 — impedir que a cobra saia do tabuleiro
    # board_width = state.board.width
    # board_height = state.board.height

    # TODO: Passo 2 — impedir que a cobra bata no próprio corpo
    # my_body = state.you.body

    # TODO: Passo 3 — impedir que a cobra bata nas adversárias
    # opponents = state.board.snakes

    # Sobrou alguma direção segura?
    safe_moves = [direction for direction, safe in is_move_safe.items() if safe]

    if not safe_moves:
        # Emergência: todas as direções são perigosas.
        # Escolhemos uma ao acaso entre as 4 — melhor do que travar.
        all_moves = ["up", "down", "left", "right"]
        fallback = random.choice(all_moves)
        logger.info("MOVE %d: sem saída! emergência -> %s", state.turn, fallback)
        return MoveResponse(move=fallback)

    # Escolhe uma direção segura ao acaso.
    chosen = random.choice(safe_moves)

    # TODO: Passo 4 — ir atrás da comida em vez de sortear, para não morrer de fome
    # food = state.board.food

    logger.info("MOVE %d: %s", state.turn, chosen)
    return MoveResponse(move=chosen)
