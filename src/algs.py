import numpy as np
import matplotlib.pyplot as plt
import random

from new_env import TakeTheLEnv

env = TakeTheLEnv()


qtable = np.zeros((env.observation_space.n, env.action_space.n))
print(qtable)


total_episodes = 500  # the total number of episodes to run
max_steps = 100  # the maximum number of steps per episode

learning_rate = 0.5  # the learning rate

gamma = 0.6  # the discount factor

# the range for the exploration parameter epsilon
epsilon = 0.2
min_epsilon = 0.01
max_epsilon = 1.0
decay_rate = 0.01

rewards = []
epsilons = []


def choose_action(state):
    exp_exp_tradeoff = random.uniform(0, 1)

    if exp_exp_tradeoff < epsilon:
        action = env.action_space.sample()
    else:
        action = np.argmax(qtable[state, :])
        # print(f"action is {action}")
    return action


def update_qlearning(state, new_state, reward, action):
    qtable[state, action] = qtable[state, action] + learning_rate * (
        reward + gamma * np.max(qtable[new_state, :]) - qtable[state, action]
    )


def update_sarsa(state, new_state, reward, action, new_action):
    qtable[state, action] = qtable[state, action] + learning_rate * (
        reward + gamma * qtable[new_state, new_action] - qtable[state, action]
    )


def qlearn(sarsa):
    global qtable
    for episode in range(total_episodes):
        state = env.reset()
        done = False
        total_rewards = 0

        for _ in range(max_steps):
            # Converting the state to a position on the table
            action = choose_action(state)

            new_state, reward, done, info = env.step(action)

            if sarsa:
                new_action = choose_action(new_state)
                update_sarsa(state, new_state, reward, action, new_action)
            else:
                update_qlearning(state, new_state, reward, action)

            total_rewards += reward

            state = new_state
            env.set_state(env.from_idx(new_state))

            if done:
                if total_rewards < 0:
                    print("Failed episode:", episode)
                env.render()
                print("Total reward for episode {}: {}".format(episode, total_rewards))
                break

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(
            -decay_rate * episode
        )
        rewards.append(total_rewards)
        epsilons.append(epsilon)

    print("Score/time: " + str(sum(rewards) / total_episodes))
    print(qtable)

    x = range(total_episodes)
    plt.plot(x, rewards)
    plt.xlabel("Episode")
    plt.ylabel("Training total reward")
    plt.title("Total rewards over all episodes in training")
    plt.show()

    plt.plot(epsilons)
    plt.xlabel("Episode")
    plt.ylabel("Epsilon")
    plt.title("Epsilon for episode")
    plt.show()

    qtable = np.zeros((env.observation_space.n, env.action_space.n))
    rewards.clear()
    epsilons.clear()
