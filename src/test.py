import numpy
from stable_baselines3.dqn.dqn import DQN

from new_env import TakeTheLEnv


def main():
    print("DQN")
    env = TakeTheLEnv()
    model = DQN("MlpPolicy", env)
    model.learn(total_timesteps=10000)
    obs = env.reset()

    for _ in range(1000):
        action, _ = model.predict(numpy.asarray(obs), deterministic=True)
        obs, _, done, _ = env.step(action)
        env.set_state(env.from_idx(obs))
        env.render()
        if done == True:
            obs = env.reset()
            break
    # action, _ = model.predict(numpy.asarray(state), deterministic=True)

    # print(f"After predict, action is {action} and states is {states}")

    # state, reward, done, _ = env.step(state, env.get_action_idx(action))
    # env.render()
    # if done:
    #    break


if __name__ == "__main__":
    main()
