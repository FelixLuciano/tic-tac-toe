# Copyright © 2023 Farama Foundation
# Tic Tac Toe
# https://pettingzoo.farama.org/environments/classic/tictactoe/

from pettingzoo.classic import tictactoe_v3
from pettingzoo.classic.tictactoe.board import Board
from pettingzoo.utils.wrappers import OrderEnforcingWrapper

import utils


def main():
    env = tictactoe_v3.raw_env("human", 256)

    env.reset()

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            break

        if agent == "player_1":
            action = play_random_agent(agent, env, observation)
        else:
            action = play_min_max_agent(agent, env)

        print(agent, "-", action)
        env.step(action)

    for agent, value in env.rewards.items():
        if value == 1:
            print(f"Agent", agent, "WINS!")
        elif value == -1:
            print(f"Agent", agent, "LOSES!")
        else:
            print(f"Agent", agent, "got a DRAW!")


def play_random_agent(agent: str, env: OrderEnforcingWrapper, observation: any):
    return env.action_space(agent).sample(observation["action_mask"])


def play_min_max_agent(agent: str, env: OrderEnforcingWrapper):
    return play_max_agent(utils.get_agent(agent), env.board)[1]


def play_min_agent(agent: str, board: Board):
    rewards = []

    for i, x in enumerate(board.squares):
        if x == 0:
            next_board, winner = utils.get_turn_board_and_winner(board, agent, i)

            if winner == 1:
                reward = -1024
            elif winner == 2:
                reward = 1024
            elif next_board.check_game_over():
                reward = 0
            else:
                reward = play_max_agent(utils.get_rival_agent(agent), next_board)[0] / 2
        else:
            reward = 2048

        rewards.append(reward)

    reward_min = 2048
    arg_min = 0

    for index, reward in enumerate(rewards):
        if board.squares[index] != 0:
            continue

        if reward < reward_min:
            reward_min = reward
            arg_min = index

    return reward_min, arg_min


def play_max_agent(agent: str, board: Board):
    rewards = []

    for i, x in enumerate(board.squares):
        if x == 0:
            next_board, winner = utils.get_turn_board_and_winner(board, agent, i)

            if winner == 1:
                reward = -1024
            elif winner == 2:
                reward = 1024
            elif next_board.check_game_over():
                reward = 0
            else:
                reward = play_min_agent(utils.get_rival_agent(agent), next_board)[0] / 2
        else:
            reward = -2048

        rewards.append(reward)

    reward_max = -2048
    arg_max = 0

    for index, reward in enumerate(rewards):
        if board.squares[index] != 0:
            continue

        if reward > reward_max:
            reward_max = reward
            arg_max = index

    return reward_max, arg_max


if __name__ == "__main__":
    main()
