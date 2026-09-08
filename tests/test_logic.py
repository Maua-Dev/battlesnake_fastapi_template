"""Testes da lógica da sua cobra. Rode com `pytest`.

Conforme você for implementando os TODOs de src/logic.py, escreva testes
novos aqui: eles rodam no GitHub Actions antes de cada deploy.
"""

import pytest
from fastapi.testclient import TestClient

from src.logic import end, info, move, start
from src.main import app

DIRECOES_VALIDAS = ["up", "down", "left", "right"]

client = TestClient(app)


def game_state(head: dict, neck: dict) -> dict:
    """Monta um estado de jogo mínimo, com a cobra deitada entre `head` e `neck`."""
    you = {
        "id": "minha-cobra",
        "name": "MinhaCobra",
        "health": 100,
        "body": [head, neck, {"x": neck["x"], "y": neck["y"] - 1}],
        "head": head,
        "length": 3,
        "latency": "50",
        "shout": "",
    }

    return {
        "game": {
            "id": "partida-de-teste",
            "ruleset": {"name": "standard", "version": "v1.2.3"},
            "map": "standard",
            "timeout": 500,
        },
        "turn": 4,
        "board": {
            "height": 11,
            "width": 11,
            "food": [{"x": 5, "y": 5}],
            "hazards": [],
            "snakes": [you],
        },
        "you": you,
    }


ESTADO_PADRAO = game_state({"x": 5, "y": 4}, {"x": 4, "y": 4})


# ---------------------------------------------------------------------------
# Lógica pura
# ---------------------------------------------------------------------------


def test_info_devolve_os_campos_obrigatorios():
    resposta = info()

    assert resposta["apiversion"] == "1"
    assert "author" in resposta
    assert "color" in resposta
    assert "head" in resposta
    assert "tail" in resposta


def test_move_devolve_sempre_uma_direcao_valida():
    for _ in range(50):
        assert move(ESTADO_PADRAO)["move"] in DIRECOES_VALIDAS


@pytest.mark.parametrize(
    "neck, proibida",
    [
        ({"x": 4, "y": 4}, "left"),  # pescoço à esquerda da cabeça
        ({"x": 6, "y": 4}, "right"),  # pescoço à direita da cabeça
        ({"x": 5, "y": 3}, "down"),  # pescoço abaixo da cabeça
        ({"x": 5, "y": 5}, "up"),  # pescoço acima da cabeça
    ],
)
def test_move_nunca_volta_por_cima_do_pescoco(neck, proibida):
    estado = game_state({"x": 5, "y": 4}, neck)

    # O movimento é sorteado, então repetimos para pegar qualquer chance de a
    # direção proibida escapar.
    for _ in range(50):
        direcao = move(estado)["move"]

        assert direcao in DIRECOES_VALIDAS
        assert direcao != proibida, f"a cobra andou para trás ({proibida})"


def test_start_e_end_nao_quebram_com_um_estado_valido():
    assert start(ESTADO_PADRAO) is None
    assert end(ESTADO_PADRAO) is None


# ---------------------------------------------------------------------------
# Integração: rotas da API, com e sem o prefixo do stage
#
# O que estes testes protegem é o middleware de src/main.py. Se o caminho
# chegar com o nome do stage na frente ("/dev/move") e o middleware sumir, a
# requisição vira 404 e a cobra deixa de responder a jogada.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("rota", ["/", "/dev/", "/dev"])
def test_rota_de_info(rota):
    resposta = client.get(rota)

    assert resposta.status_code == 200
    assert resposta.json()["apiversion"] == "1"


@pytest.mark.parametrize("rota", ["/move", "/dev/move"])
def test_rota_de_move(rota):
    resposta = client.post(rota, json=ESTADO_PADRAO)

    assert resposta.status_code == 200
    assert resposta.json()["move"] in DIRECOES_VALIDAS


@pytest.mark.parametrize("rota", ["/start", "/dev/start", "/end", "/dev/end"])
def test_rotas_de_start_e_end(rota):
    resposta = client.post(rota, json=ESTADO_PADRAO)

    assert resposta.status_code == 200
    assert resposta.json() == "ok"


def test_move_pela_api_nunca_volta_por_cima_do_pescoco():
    # Pescoço à esquerda da cabeça: "left" seria andar para trás.
    estado = game_state({"x": 5, "y": 4}, {"x": 4, "y": 4})

    for _ in range(50):
        direcao = client.post("/dev/move", json=estado).json()["move"]

        assert direcao in DIRECOES_VALIDAS
        assert direcao != "left"
