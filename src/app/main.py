"""Ponte entre o AWS Lambda e a lógica da sua cobra.

Você NÃO precisa mexer aqui. Este arquivo define os endpoints FastAPI e
repassa as chamadas para logic.py.

Rotas da API (https://docs.battlesnake.com/api):
  GET  /        -> aparência da cobra
  POST /start   -> a partida começou
  POST /move    -> escolha a jogada deste turno
  POST /end     -> a partida acabou
"""
from fastapi import FastAPI
from mangum import Mangum
from . import logic
from .models import GameState, MoveResponse

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    """GET / — informações e aparência da cobra."""
    return logic.info()


@app.post("/start")
def start(state: GameState) -> str:
    """POST /start — chamado no início de cada partida."""
    logic.start(state)
    return "ok"


@app.post("/move")
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