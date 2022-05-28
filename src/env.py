from gym import Env
from typing import Tuple
from board import Board, is_complete


class TakeTheLEnv(Env):

    metadata = {"render_modes": ["human", "rgb_array"], "rendder_fps": 50}

    def __init__(self, difficulty: int) -> None:
        self.state = Board(difficulty)
        self.difficulty = difficulty
        self.pos = self.state.start

    # TODO: Complete this definition with actions
    def step(self, action) -> Tuple[Board, float, bool, dict]:
        done = is_complete(self.pos, self.state.goal)
        return Board(0), 0.0, done, {}

    def reset(self):
        self.state.reset()

    # HACK: For mow it is using print. Later change to pygame
    def render(self, mode="human"):
        print(self.state)

    # action_space: spaces.Space[ActType] =
    # observation_space: spaces.Space[ObsType] = {}
