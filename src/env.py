from gym import Env
from typing import Tuple
from board import Board, is_complete


class TakeTheLEnv(Env):

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self, difficulty: int) -> None:
        self.state = Board(difficulty)
        self.difficulty = difficulty
        self.pos = self.state.start

    def step(self, action: int) -> Tuple[Board, float, bool, dict]:
        movement: Tuple[int, int] = self.state.ACTIONS[action]
        reward, info = self.perform_step(movement)
        done = is_complete(self.pos, self.state.goal)
        return self.state, reward, done, info

    # NOTE: When info should be added, it should be in this method
    def perform_step(self, step: Tuple[int, int]) -> Tuple[float, dict]:
        new_pos = (self.pos[0] + step[0], self.pos[1] + step[1])
        self.state.visit(new_pos)
        reward: float = self.state.evaluate_board_state()
        return reward, {}

    def reset(self):
        self.state.reset()

    # NOTE: For mow it is using print. Later change to pygame
    def render(self, mode="human"):
        print(self.state)

    # action_space: spaces.Space[ActType] =
    # observation_space: spaces.Space[ObsType] = {}
