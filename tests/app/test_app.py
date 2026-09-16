"""Testes de integração: percorrem o caminho completo HTTP -> endpoint -> logic.

Rode com: pytest
"""
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

DIRECOES = ["up", "down", "left", "right"]


# --- Estado de jogo mínimo para os testes ---

def game_state(head: dict, neck: dict) -> dict:
    """Monta um estado de jogo mínimo com a cobra deitada entre head e neck."""
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


# T1 — info retorna os campos obrigatórios
class TestInfo:
    def test_retorna_status_200(self):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_retorna_campos_obrigatorios(self):
        resp = client.get("/")
        body = resp.json()
        assert body["apiversion"] == "1"
        assert "author" in body
        assert "color" in body
        assert "head" in body
        assert "tail" in body


# T2 — move retorna uma direção válida
class TestMove:
    def test_retorna_status_200(self):
        resp = client.post("/move", json=ESTADO_PADRAO)
        assert resp.status_code == 200

    def test_retorna_direcao_valida(self):
        for _ in range(50):
            resp = client.post("/move", json=ESTADO_PADRAO)
            assert resp.json()["move"] in DIRECOES

    # T3 — nunca volta contra o pescoço
    def test_nunca_volta_contra_o_pescoco(self):
        casos = [
            ({"x": 4, "y": 4}, "left"),   # pescoço à esquerda
            ({"x": 6, "y": 4}, "right"),  # pescoço à direita
            ({"x": 5, "y": 3}, "down"),   # pescoço abaixo
            ({"x": 5, "y": 5}, "up"),     # pescoço acima
        ]
        for neck, proibida in casos:
            state = game_state({"x": 5, "y": 4}, neck)
            for _ in range(50):
                resp = client.post("/move", json=state)
                assert resp.json()["move"] != proibida, (
                    f"a cobra voltou contra o pescoço ({proibida})"
                )

    # T4 — evita parede quando tem opção
    def test_evita_parede_quando_tem_opcao(self):
        # Cobra no canto inferior esquerdo, pescoço à direita
        # Não pode ir left (x=-1) nem down (y=-1) nem right (pescoço)
        # Só pode ir up
        state = game_state({"x": 0, "y": 0}, {"x": 1, "y": 0})
        for _ in range(50):
            resp = client.post("/move", json=state)
            chosen = resp.json()["move"]
            assert chosen != "left", "foi para fora do tabuleiro (esquerda)"
            assert chosen != "down", "foi para fora do tabuleiro (baixo)"

    # T5 — evita próprio corpo quando tem opção
    def test_evita_proprio_corpo_quando_tem_opcao(self):
        head = {"x": 5, "y": 4}
        neck = {"x": 4, "y": 4}   # pescoço à esquerda
        body_block = {"x": 5, "y": 5}  # corpo acima
        state = game_state(head, neck)
        state["you"]["body"] = [head, neck, body_block, {"x": 4, "y": 3}]
        state["board"]["snakes"] = [state["you"]]
        for _ in range(50):
            resp = client.post("/move", json=state)
            chosen = resp.json()["move"]
            assert chosen != "left", "voltou pelo pescoço"
            assert chosen != "up", "bateu no próprio corpo"

    # T6 — comportamento sem safe moves
    def test_comportamento_sem_safe_moves(self):
        # Cobra com todas as direções inseguras — não deve lançar exceção
        head = {"x": 0, "y": 0}
        neck = {"x": 0, "y": 1}  # pescoço acima (bloqueia up)
        state = game_state(head, neck)
        # Adiciona corpo à direita para bloquear right
        state["you"]["body"] = [head, neck, {"x": 1, "y": 0}, {"x": 0, "y": 1}]
        state["board"]["snakes"] = [state["you"]]
        resp = client.post("/move", json=state)
        assert resp.status_code == 200
        assert resp.json()["move"] in DIRECOES


# start e end
class TestStartEnd:
    def test_start_retorna_ok(self):
        resp = client.post("/start", json=ESTADO_PADRAO)
        assert resp.status_code == 200

    def test_end_retorna_ok(self):
        resp = client.post("/end", json=ESTADO_PADRAO)
        assert resp.status_code == 200