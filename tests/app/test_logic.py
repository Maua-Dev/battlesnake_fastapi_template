"""Testes unitários diretos da lógica da cobra.

Rode com: pytest
"""
import pytest
from src.app.logic import info, start, end, get_move
from src.app.models import GameState, Board, Snake, Coord, Game

DIRECOES = ["up", "down", "left", "right"]


def make_state(head: tuple[int, int], neck: tuple[int, int]) -> GameState:
    """Monta um estado de jogo mínimo para os testes."""
    hx, hy = head
    nx, ny = neck
    you = Snake(
        id="minha-cobra",
        name="MinhaCobra",
        health=100,
        body=[
            Coord(x=hx, y=hy),
            Coord(x=nx, y=ny),
            Coord(x=nx, y=ny - 1),
        ],
        head=Coord(x=hx, y=hy),
        length=3,
    )
    return GameState(
        game=Game(id="partida-de-teste", timeout=500),
        turn=4,
        board=Board(
            height=11,
            width=11,
            food=[Coord(x=5, y=5)],
            hazards=[],
            snakes=[you],
        ),
        you=you,
    )


# T1 — info retorna campos obrigatórios
def test_info_retorna_campos_obrigatorios():
    response = info()
    assert response["apiversion"] == "1"
    assert "author" in response
    assert "color" in response
    assert "head" in response
    assert "tail" in response


# T2 — get_move retorna direção válida
def test_get_move_retorna_direcao_valida():
    state = make_state((5, 4), (4, 4))
    for _ in range(50):
        result = get_move(state)
        assert result.move in DIRECOES


# T3 — nunca volta contra o pescoço
@pytest.mark.parametrize("neck,proibida", [
    ((4, 4), "left"),   # pescoço à esquerda
    ((6, 4), "right"),  # pescoço à direita
    ((5, 3), "down"),   # pescoço abaixo
    ((5, 5), "up"),     # pescoço acima
])
def test_nunca_volta_contra_pescoco(neck, proibida):
    state = make_state((5, 4), neck)
    for _ in range(50):
        result = get_move(state)
        assert result.move != proibida, f"a cobra voltou contra o pescoço ({proibida})"


# T4 — evita parede quando tem opção (os TODOs ainda não estão implementados,
# então este teste verifica só que a função retorna sem erros)
def test_retorna_direcao_valida_na_borda():
    state = make_state((0, 0), (1, 0))
    for _ in range(20):
        result = get_move(state)
        assert result.move in DIRECOES


# T6 — sem safe moves -> retorna direção válida sem lançar exceção
def test_comportamento_sem_safe_moves():
    state = make_state((0, 0), (0, 1))
    # Adiciona corpo à direita para bloquear todas as saídas
    state.you.body = [
        Coord(x=0, y=0),
        Coord(x=0, y=1),
        Coord(x=1, y=0),
    ]
    state.board.snakes = [state.you]
    result = get_move(state)
    assert result.move in DIRECOES


# start e end não lançam exceções
def test_start_nao_lanca_excecao():
    state = make_state((5, 4), (4, 4))
    start(state)  # deve completar sem exceção


def test_end_nao_lanca_excecao():
    state = make_state((5, 4), (4, 4))
    end(state)  # deve completar sem exceção
