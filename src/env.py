from copy import deepcopy
from typing import Tuple
from gym import Env, spaces
import numpy as np

from utils import manhattan_distance


BOARD_ROWS = 4
BOARD_COLS = 4
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


class TakeTheLEnv(Env):

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self) -> None:
        self.board: np.ndarray = np.zeros([BOARD_ROWS, BOARD_COLS], dtype=np.int32)
        self.size: int = len(self.board)
        self.start_state: Tuple[int, int] = (self.size - 1, 0)
        self.goal_state: Tuple[int, int] = (0, self.size - 1)
        self.board[self.start_state[0]][self.start_state[1]] = 1

        # Gym specific variables
        self.action_space: spaces.Discrete = spaces.Discrete(4)
        self.observation_space: spaces.Discrete = spaces.Discrete(self.size**2)

    def reset(self) -> None:
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS], dtype=np.int32)

    # NOTE: For mow it is using print. Later change to pygame
    def render(self) -> None:
        self.showBoard()

    def close(self) -> None:
        return super().close()

    def step(
        self, state: Tuple[int, int], action: int | np.intp
    ) -> Tuple[Tuple[int, int], float, bool, dict]:
        new_pos: Tuple[int, int] = state
        if action == LEFT:
            new_pos = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_pos = (state[0], state[1] + 1)
        elif action == DOWN:
            new_pos = (state[0] + 1, state[1])
        elif action == UP:
            new_pos = (state[0] - 1, state[1])

        if self.check_bounds(new_pos):
            new_state = new_pos
        else:
            new_state = state

        self.board[new_state[0]][new_state[1]] = 1

        done: bool = self.reached_end(new_state)
        reward: float = self.determine_reward(new_state)
        info: dict = {}

        return new_state, reward, done, info

    def reached_end(self, state) -> bool:
        return state == self.goal_state

    def check_bounds(self, pos) -> bool:
        return not (
            pos[0] < 0 or pos[1] < 0 or pos[0] >= self.size or pos[1] >= self.size
        )

    def determine_reward(self, state) -> float:
        if self.board[state[0]][state[1]] == 0:
            return 0

    def showBoard(self) -> None:
        for i in range(0, BOARD_ROWS):
            print("-----------------")
            out = "| "
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = "*"
                elif self.board[i, j] == -1:
                    token = "z"
                elif self.board[i, j] == 0:
                    token = "0"
                else:
                    token = " "

                out += token + " | "
            print(out)
        print("-----------------")
