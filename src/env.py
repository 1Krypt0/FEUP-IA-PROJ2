from copy import deepcopy
from typing import Tuple
from gym import Env, spaces
import numpy as np


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
        self.state: Tuple[int, int] = deepcopy(self.start_state)

        # Gym specific variables
        self.action_space: spaces.Discrete = spaces.Discrete(4)
        self.observation_space: spaces.Discrete = spaces.Discrete(self.size**2)

    def reset(self) -> None:
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS], dtype=np.int32)
        self.state = deepcopy(self.start_state)

    # NOTE: For mow it is using print. Later change to pygame
    def render(self) -> None:
        self.showBoard()

    def close(self) -> None:
        return super().close()

    def step(self, action) -> Tuple[Tuple[int, int], float, bool, dict]:
        new_pos: Tuple[int, int] = self.state
        if action == LEFT:
            new_pos = (self.state[0], self.state[1] - 1)
        elif action == RIGHT:
            new_pos = (self.state[0], self.state[1] + 1)
        elif action == DOWN:
            new_pos = (self.state[0] + 1, self.state[1])
        elif action == UP:
            new_pos = (self.state[0] - 1, self.state[1])

        if self.check_bounds(new_pos):
            new_state = new_pos
        else:
            new_state = self.state

        done: bool = self.reached_end()
        reward: float = self.determine_reward()
        info: dict = {}

        return new_state, reward, done, info

    def reached_end(self) -> bool:
        return self.state == self.goal_state

    def check_bounds(self, pos) -> bool:
        return not (
            pos[0] < 0 or pos[1] < 0 or pos[0] >= self.size or pos[1] >= self.size
        )

    def determine_reward(self) -> float:
        return -0.1 * (self.goal_state[0] - self.state[0]) 
        # if self.reached_end():
        #     return 1
        # else:
        #     return 0

    def showBoard(self) -> None:
        self.board[self.state] = 1
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
