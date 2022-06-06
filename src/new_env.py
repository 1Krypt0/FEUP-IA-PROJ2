import numpy as np
from utils import manhattan_distance
from gym.core import Env
from gym.spaces.discrete import Discrete


RED = "\033[31m"
RESET = "\033[0m"

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


class TakeTheLEnv(Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self) -> None:
        super(TakeTheLEnv, self).__init__()

        self.board = [[1, 2, 2, 0], [1, 0, 2, 0], [1, 1, 2, 0], [0, 0, 0, 0]]
        self.size = len(self.board)
        self.state = (self.size - 1, 0)
        self.action_space = Discrete(4)
        self.observation_space = Discrete(self.size**2)

    def set_board(self, new_board) -> None:
        self.board = new_board
        self.reset()

    def to_idx(self, pos):
        return self.size * pos[0] + pos[1]

    def from_idx(self, idx):
        return (idx // self.size, idx % self.size)

    def increment(self, pos, action):
        row, col = pos
        if action == LEFT:
            col = max(col - 1, 0)
        elif action == DOWN:
            row = min(row + 1, self.size - 1)
        elif action == RIGHT:
            col = min(col + 1, self.size - 1)
        elif action == UP:
            row = max(row - 1, 0)
        return (row, col)

    def step(self, action):
        new_pos = self.increment(self.state, action)

        new_state = self.to_idx(new_pos)
        reward = self.give_reward(new_pos)
        done = new_pos == (0, self.size - 1)
        self.visited[new_pos[0]][new_pos[1]] = 1
        if self.board[new_pos[0]][new_pos[1]] != 0:
            self.visited_shapes.add(self.board[new_pos[0]][new_pos[1]])

        return new_state, reward, done, {}

    def set_state(self, new_state):
        self.state = new_state

    def give_reward(self, new_pos):
        value = self.board[new_pos[0]][new_pos[1]]
        is_visited = self.visited[new_pos[0]][new_pos[1]] == 1
        if is_visited:
            return -50
        if value in self.visited_shapes:
            return -50
        if new_pos == (0, self.size - 1) and self.visited_shapes == self.all_shapes:
            return 10
        if new_pos == (0, self.size - 1) and self.visited_shapes != self.all_shapes:
            return -50
        if value not in self.visited_shapes and value != 0:
            return 10
        if value == 0:
            return -0.25 * len(self.all_shapes)
        else:
            return -1

    def reset(self):
        self.size = len(self.board)
        self.action_space = Discrete(len(self.board[0]))
        self.observation_space = Discrete(self.size**2)
        self.state = (self.size - 1, 0)
        self.visited = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.visited[self.state[0]][self.state[1]] = 1
        self.visited_shapes = set()
        self.all_shapes = self.determine_shapes()
        return self.to_idx(self.state)

    def render(self, mode="human"):
        self.show_board()

    def close(self):
        return super().close()

    def determine_shapes(self) -> set:
        """
        Determines shapes from board content
            Parameters:
                board (list[list[int]]): the content of the board

            Returns:
                shapes (set): the set of different shapes in the board
        """

        final = set()
        for line in self.board:
            for num in line:
                if num not in final and num != 0:
                    final.add(num)
        return final

    def show_board(self) -> None:
        padding_left = 3
        padding_right = 2
        padding_top = "  _" + self.size * "____"
        padding_bot = "  ‾" + self.size * "‾‾‾‾"
        number_space = "   "
        # if len(self.all_shapes) >= 10:
        #     padding_left += 1
        #     padding_right += 1
        #     padding_top += self.size * "_"
        #     padding_bot += self.size * "‾"
        #     number_space = "    "

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
