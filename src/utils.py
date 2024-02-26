import typing as T
from copy import deepcopy

from pettingzoo.classic.tictactoe.board import Board


def get_rival_name(agent: T.Literal["player_1", "player_2"]):
    return "player_1" if agent == "player_2" else "player_2"


def get_agent(agent: T.Literal["player_1", "player_2"]):
    return 0 if agent == "player_1" else 1


def get_rival_agent(agent: T.Literal[0, 1]):
    return 0 if agent == 1 else 0


def get_rival(agent: T.Literal["player_1", "player_2"]):
    return 0 if agent == 1 else 2


def get_turn_board_and_winner(board: Board, agent: int, position: int):
    next_board = deepcopy(board)

    next_board.play_turn(agent, position)
    next_board.calculate_winners()

    return next_board, next_board.check_for_winner()


def get_min_and_argmin(values, mask):
    value_min = max(values)
    argmin = 0

    for index, value in enumerate(values):
        if mask[index] != 0:
            continue

        if value < value_min:
            value_min = value
            argmin = index

    return value_min, argmin


def get_max_and_argmax(values, mask):
    value_max = min(values)
    argmax = 0

    for index, value in enumerate(values):
        if mask[index] != 0:
            continue

        if value > value_max:
            value_max = value
            argmax = index

    return value_max, argmax
