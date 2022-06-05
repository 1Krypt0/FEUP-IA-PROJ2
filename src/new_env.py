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

        self.board = np.zeros([4, 4])  # [
        #     [2, 2, 0, 0, 0],
        #     [2, 0, 1, 4, 4],
        #     [2, 0, 1, 3, 4],
        #     [0, 1, 1, 3, 4],
        #     [0, 0, 3, 3, 0],
        # ]
        self.size = len(self.board)
        self.state = (self.size - 1, 0)
        self.action_space = Discrete(4)
        self.observation_space = Discrete(self.size**2)

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
        self.visited[new_pos[0]][new_pos[1]] = 1
        reward = self.give_reward()
        done = self.state == (0, self.size - 1)
        return new_state, reward, done, {}

    def set_state(self, new_state):
        self.state = new_state

    def give_reward(self):
        # value = self.board[self.state[0]][self.state[1]]
        if self.state == (0, self.size - 1):
            return 10
        else:
            return -1  # / manhattan_distance(self.state, (0, self.size - 1))

    def reset(self):
        self.state = (self.size - 1, 0)
        self.visited = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.visited[self.state[0]][self.state[1]] = 1
        # self.all_shapes = set()
        return self.to_idx(self.state)

    def render(self, mode="human"):
        print(self.board)
        # self.show_board()

    def close(self):
        return super().close()

    def show_board(self) -> None:
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
