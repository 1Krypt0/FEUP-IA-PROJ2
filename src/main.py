from env import TakeTheLEnv
import algs


def main():

    # print("Q-LEARNING")
    # algs.qlearn(False)

    print("SARSA")
    algs.qlearn(True)


if __name__ == "__main__":
    main()
