from typing import List, Set, Tuple
from gym import Env, spaces
import numpy as np

RED = "\033[31m"
RESET = "\033[0m"
BOARD_ROWS = 4
BOARD_COLS = 4
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


class TakeTheLEnv(Env):
    def __init__(self) -> None:
        self.board: List[List[int]] = [
            [2, 2, 0, 0, 0],
            [2, 0, 1, 4, 4],
            [2, 0, 1, 3, 4],
            [0, 1, 1, 3, 4],
            [0, 0, 3, 3, 0],
        ]
        self.size: int = len(self.board)
        self.start_state: Tuple[int, int] = (self.size - 1, 0)
        self.goal_state: Tuple[int, int] = (0, self.size - 1)
        self.visited_shapes = set()
        self.visited = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.all_shapes = self.determine_shapes(self.board)

        self.visited[self.start_state[0]][self.start_state[1]] = 1

        # Gym specific variables
        self.action_space: spaces.Discrete = spaces.Discrete(4)
        self.observation_space: spaces.Discrete = spaces.Discrete(self.size**2)

    def reset(self) -> None:
        self.board = [
            [2, 2, 0, 0, 0],
            [2, 0, 1, 4, 4],
            [2, 0, 1, 3, 4],
            [0, 1, 1, 3, 4],
            [0, 0, 3, 3, 0],
        ]
        self.visited = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.visited[self.start_state[0]][self.start_state[1]] = 1

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

        if self.board[new_state[0]][new_state[1]] != 0:
            self.visited_shapes.add(self.board[new_state[0]][new_state[1]])

        self.visited[new_state[0]][new_state[1]] = 1

        return new_state, reward, done, info

    def reached_end(self, state) -> bool:
        return state == self.goal_state

    def check_bounds(self, pos) -> bool:
        return not (
            pos[0] < 0 or pos[1] < 0 or pos[0] >= self.size or pos[1] >= self.size
        )

    def determine_reward(self, state) -> float:
        val = self.board[state[0]][state[1]]

        # won game
        if self.reached_end(state) and self.all_visited():
            return 10
        if self.reached_end(state) and (not self.all_visited()):
            return -1
        # didn't win game yet
        # if self.visited[state[0]][state[1]] == 1:
        #    return -1
        if val == 0 and (self.visited[state[0]][state[1]] == 1):
            return -1
        if val in self.visited_shapes:
            return -5
        if val not in self.visited_shapes:
            return 3
        else:
            return -1

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
        return self.visited_shapes == self.all_shapes

    def showBoard(self) -> None:
        padding_left = 3
        padding_right = 2
        padding_top = "  _" + self.size * "____"
        padding_bot = "  ‾" + self.size * "‾‾‾‾"
        number_space = "   "
        if len(self.all_shapes) >= 10:
            padding_left += 1
            padding_right += 1
            padding_top += self.size * "_"
            padding_bot += self.size * "‾"
            number_space = "    "

        final = "\n "
        for i in range(self.size):
            final += number_space + str(i)
        final += "\n"
        final += padding_top
        final += "\n"
        for line in range(self.size):
            final += str(line) + " "
            for col in range(self.size):
                final += (
                    "|"
                    + RED * self.visited[line][col]
                    + str(self.board[line][col])
                    .rjust(padding_right)
                    .ljust(padding_left)
                    + RESET
                )
            final += "|\n"
        final += padding_bot
        final += "\n"
        print(final)
