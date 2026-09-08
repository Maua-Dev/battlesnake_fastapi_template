# Ponte entre o AWS Lambda e a lógica da sua cobra.
#
# Você NÃO precisa mexer aqui. Este arquivo monta a aplicação FastAPI com as
# quatro rotas do Battlesnake e a embrulha com o Mangum, que traduz o evento
# do API Gateway em uma requisição HTTP comum.
#
# Rotas da API (https://docs.battlesnake.com/api):
#   GET  /        -> aparência da cobra
#   POST /start   -> a partida começou
#   POST /move    -> escolha a jogada deste turno
#   POST /end     -> a partida acabou

import typing

from fastapi import FastAPI, Request
from mangum import Mangum

from src import logic

app = FastAPI(
    title="Battlesnake",
    description="Template de Battlesnake da Dev. Community Mauá",
    version="1.0.0",
)

# Nomes de stage que o API Gateway pode colocar na frente do caminho.
STAGE_PREFIXES = ("dev", "homolog", "prod", "staging")


@app.middleware("http")
async def remove_stage_prefix(request: Request, call_next):
    """Remove o prefixo do stage (ex.: /dev, /staging, /prod) se presente.

    Dependendo de como a API é exposta, o caminho pode chegar ao FastAPI com o
    nome do stage na frente ("/dev/move" em vez de "/move"). Sem esta
    normalização o POST /move não casa com nenhuma rota e vira 404, o que faz
    a cobra ser eliminada por não responder a jogada.
    """
    first, _, rest = request.scope["path"].lstrip("/").partition("/")

    if first in STAGE_PREFIXES:
        request.scope["path"] = "/" + rest

    return await call_next(request)


@app.get("/")
def on_info() -> typing.Dict:
    return logic.info()


@app.post("/start")
def on_start(game_state: typing.Dict) -> str:
    logic.start(game_state)
    return "ok"


@app.post("/move")
def on_move(game_state: typing.Dict) -> typing.Dict:
    return logic.move(game_state)


@app.post("/end")
def on_end(game_state: typing.Dict) -> str:
    logic.end(game_state)
    return "ok"


# É este nome que o Terraform configura como handler da Lambda
# (veja terraform/app/main.tf: handler = "src.main.handler").
handler = Mangum(app, lifespan="off")
