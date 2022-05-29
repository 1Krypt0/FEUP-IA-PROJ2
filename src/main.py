from env import TakeTheLEnv
import numpy as np
import random


def main():
    print("Loading the environment")

    env = TakeTheLEnv(1)
    env.reset()
    env.render()
    print("Environemnt loaded succesffully")

    action_size: int = env.action_space.n
    state_size: int = env.observation_space.n
    print(f"action size: {action_size}, state size: {state_size}")

    qtable = np.zeros((state_size, action_size))
    print(qtable)

    print("Checking possible actions")
    actions = env.state.get_available_actions(env.pos)
    print("Available actions are", actions)
    new_state, reward, done, info = env.step(actions[0])

    print("Reward:", reward)
    print("New State:", new_state)
    print("Done:", done)

    env.close()

    print("Setting parameters for Q-learning")
    # Set hyperparameters for Q-learning

    # @hyperparameters
    total_episodes = 200  # Total episodes
    max_steps = 99  # Max steps per episode

    learning_rate = 0.8  # Learning rate
    gamma = 0.95  # Discounting rate

    # Exploration parameters
    epsilon = 1.0  # Exploration rate
    max_epsilon = 1.0  # Exploration probability at start
    min_epsilon = 0.01  # Minimum exploration probability
    decay_rate = 0.001  # Exponential decay rate for exploration prob
    # I find that decay_rate=0.001 works much better than 0.01
    #


if __name__ == "__main__":
    main()
