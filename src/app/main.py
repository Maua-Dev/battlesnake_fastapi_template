"""Ponte entre o AWS Lambda e a lógica da sua cobra.

Você NÃO precisa mexer aqui. Este arquivo define os endpoints FastAPI e
repassa as chamadas para logic.py.

Rotas da API (https://docs.battlesnake.com/api):
  GET  /        -> aparência da cobra
  POST /start   -> a partida começou
  POST /move    -> escolha a jogada deste turno
  POST /end     -> a partida acabou
"""
from fastapi import FastAPI, Request
from mangum import Mangum
from . import logic
from .models import GameState, MoveResponse

app = FastAPI()

# Nomes de stage que o API Gateway pode colocar na frente do caminho.
STAGE_PREFIXES = ("dev", "homolog", "prod", "staging")


@app.middleware("http")
async def remove_stage_prefix(request: Request, call_next):
    """Remove o prefixo do stage (ex.: /dev, /staging) quando presente.

    Dependendo de como a API e exposta, o caminho pode chegar como "/dev/move"
    em vez de "/move". Sem esta normalizacao a rota nao casa e vira 404.
    """
    first, _, rest = request.scope["path"].lstrip("/").partition("/")

    if first in STAGE_PREFIXES:
        request.scope["path"] = "/" + rest

    return await call_next(request)


@app.get("/")
def read_root() -> dict:
    """GET / — informações e aparência da cobra."""
    return logic.info()


@app.post("/start")
def start(state: GameState) -> str:
    """POST /start — chamado no início de cada partida."""
    logic.start(state)
    return "ok"


# exclude_none tira o "shout": null da resposta — o contrato define shout
# como opcional, e nao como nulo.
@app.post("/move", response_model_exclude_none=True)
def move(state: GameState) -> MoveResponse:
    """POST /move — chamado a cada turno. Chama a lógica da cobra."""
    return logic.get_move(state)


@app.post("/end")
def end(state: GameState) -> str:
    """POST /end — chamado no fim de cada partida."""
    logic.end(state)
    return "ok"


# Handler para AWS Lambda via Mangum
handler = Mangum(app, lifespan="off")