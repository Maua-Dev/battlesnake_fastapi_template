"""Modelos Pydantic que representam o estado do jogo enviado pelo Battlesnake.

Você não precisa mexer neste arquivo, mas vale a pena ler: é o mapa
completo de tudo que a sua cobra consegue "enxergar" a cada turno.

Documentação: https://docs.battlesnake.com/api
"""
from __future__ import annotations
from typing import Any
from pydantic import BaseModel


class Coord(BaseModel):
    """Uma posição no tabuleiro. Origem (0,0) no canto inferior esquerdo."""
    x: int
    y: int


class Snake(BaseModel):
    """Uma cobra em jogo — pode ser a sua ou uma adversária."""
    id: str
    name: str
    # Vai de 0 a 100. Chegou a 0, a cobra morre de fome.
    health: int
    # Corpo inteiro, da cabeça (índice 0) até a cauda (último).
    body: list[Coord]
    head: Coord
    length: int
    latency: str | None = None
    shout: str | None = None


class Board(BaseModel):
    """O tabuleiro no turno atual."""
    height: int
    width: int
    # Comidas disponíveis. Comer devolve vida a 100 e aumenta o corpo em 1.
    food: list[Coord]
    # Casas perigosas (só aparecem em alguns modos de jogo).
    hazards: list[Coord] = []
    # Todas as cobras vivas, incluindo a sua.
    snakes: list[Snake]


class Game(BaseModel):
    """Metadados da partida."""
    id: str
    ruleset: dict[str, Any] = {}
    map: str | None = None
    # Tempo máximo, em milissegundos, para responder o /move.
    timeout: int


class GameState(BaseModel):
    """O pacote completo que chega em /start, /move e /end."""
    game: Game
    turn: int
    board: Board
    you: Snake


class MoveResponse(BaseModel):
    """Resposta do endpoint /move."""
    move: str
    shout: str | None = None
