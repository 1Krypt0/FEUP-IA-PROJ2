from env import TakeTheLEnv


def main():
    env = TakeTheLEnv(1)
    env.reset()
    env.render()
    pass


if __name__ == "__main__":
    main()
