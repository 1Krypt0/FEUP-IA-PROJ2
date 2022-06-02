import env
import numpy as np
import random

def qlearn(environment):
    qtable = np.zeros((environment.observation_space.n, environment.action_space.n))
    print(qtable)

    # the total number of episodes to run
    total_episodes = 200
    
    # the maximum number of steps per episode
    max_steps = 99
    
    # the learning rate
    learning_rate = 0.8
    
    # the discount factor
    gamma = 0.95
    
    # the range for the exploration parameter epsilon
    epsilon = 1.0
    min_epsilon = 0.01
    max_epsilon = 1.0

    # the epsilon decay rate
    decay_rate = 0.001

    rewards = []

    for episode in range(total_episodes):
        state = environment.reset()
        print(f"state: {state}")
        step = 0 
        done = False
        total_rewards = 0

        for step in range(max_steps):
            print(f"start step...")
            exp_exp_tradeoff = random.uniform(0, 1)
            print(f"exp_exp_tradeoff: {exp_exp_tradeoff}")

            if exp_exp_tradeoff > epsilon:
                print(f"qtable[state,:] {qtable[state,:]}")
                action = np.argmax(qtable[state,:])
            else:
                action = environment.action_space.sample()
                print(f"action is {action}")
            
            new_state, reward, done, info = environment.step(action)
            print(f"new_state: {new_state}, reward: {reward}, done: {done}, info: {info}")
            qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma * np.max(qtable[new_state, :]) - qtable[state, action])

            print(f'qtable: {qtable}')

            total_rewards = total_rewards + reward
            print(f'total_rewards {total_rewards}')

            state = new_state

            if done: 
                break

        epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)
        rewards.append(total_rewards)

    print ("Score/time: " +  str(sum(rewards)/total_episodes))
    print(qtable)
    print(epsilon)
        