from copy import deepcopy
from typing import List, Set, Tuple
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
        self.board: List[List[int]] = [
            [1, 1, 1, 2, 2, 0],
            [0, 3, 1, 2, 4, 0],
            [0, 3, 0, 2, 4, 5],
            [0, 3, 3, 4, 4, 5],
            [0, 6, 6, 6, 5, 5],
            [0, 0, 0, 6, 0, 0],
        ]
        self.size: int = len(self.board)
        self.start_state: Tuple[int, int] = (self.size - 1, 0)
        self.goal_state: Tuple[int, int] = (0, self.size - 1)
        self.visited = set()
        self.all_shapes = self.determine_shapes(self.board)

        # Gym specific variables
        self.action_space: spaces.Discrete = spaces.Discrete(4)
        self.observation_space: spaces.Discrete = spaces.Discrete(self.size**2)

    def reset(self) -> None:
        self.board = [
            [1, 1, 1, 2, 2, 0],
            [0, 3, 1, 2, 4, 0],
            [0, 3, 0, 2, 4, 5],
            [0, 3, 3, 4, 4, 5],
            [0, 6, 6, 6, 5, 5],
            [0, 0, 0, 6, 0, 0],
        ]

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
        val = self.board[state[0]][state[1]]
        if self.reached_end(state) and self.all_visited():
            return 50
        if self.reached_end(state) and (not self.all_visited()):
            return -25
        if val not in self.visited:
            return 10
        if val in self.visited:
            return -10
        else:
            return 0

    def determine_shapes(self, board: List[List[int]]) -> Set[int]:
        """
        Determines shapes from board content
        Parameters:
        board (list[list[int]]): the content of the board

        Returns:
        shapes (set): the set of different shapes in the board
        """
        final = set()
        for line in board:
            for num in line:
                if num not in final:
                    final.add(num)
        return final

    def all_visited(self):
        """
        Checks if the player has visited all the different shapes
        Parameters:
            board (Board): the board's content

        Return:
            all_visited (bool): whether the player has visited all the shapes
        """
        return self.visited == self.all_shapes

    # TODO: Change to fit new board style
    def showBoard(self) -> None:
        for i in range(0, BOARD_ROWS):
            print("-----------------")
            out = "| "
            for j in range(0, BOARD_COLS):
                if self.board[i][j] == 1:
                    token = "*"
                elif self.board[i][j] == -1:
                    token = "z"
                elif self.board[i][j] == 0:
                    token = "0"
                else:
                    token = " "

                out += token + " | "
            print(out)
        print("-----------------")
