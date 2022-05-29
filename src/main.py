from env import TakeTheLEnv
import numpy as np
import random


def main():
    print("Loading the environment")
    env = TakeTheLEnv()
    env.reset()
    env.render()
    print("Environemnt loaded succesffully")

    action_size: int = env.action_space.n
    state_size: int = env.observation_space.n
    print(f"action size: {action_size}, state size: {state_size}")

    env.close()


if __name__ == "__main__":
    main()
