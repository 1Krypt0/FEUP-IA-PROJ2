from gym import Env, spaces
from typing import Tuple

from gym.spaces.discrete import Discrete
from board import Board, is_complete

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


class TakeTheLEnv(Env):

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self, difficulty: int) -> None:
        self.state = Board(difficulty)
        self.difficulty = difficulty
        self.pos = self.state.start
        self.action_space: Discrete = spaces.Discrete(4)
        self.observation_space: Discrete = spaces.Discrete(self.state.size**2)

    def step(self, action: int) -> Tuple[Board, float, bool, dict]:
        movement: Tuple[int, int] = self.state.ACTIONS[action]
        reward, info = self.perform_step(movement)
        done = is_complete(self.pos, self.state.goal)
        return self.state, reward, done, info

    def reset(self):
        self.state.reset()
        self.state.visit(self.state.start)

    # NOTE: For mow it is using print. Later change to pygame
    def render(self, mode="human"):
        print(self.state)

    # NOTE: When info should be added, it should be in this method
    def perform_step(self, step: Tuple[int, int]) -> Tuple[float, dict]:
        new_pos = (self.pos[0] + step[0], self.pos[1] + step[1])
        self.state.visit(new_pos)
        reward: float = self.state.evaluate_board_state_1(new_pos)
        return reward, {}
