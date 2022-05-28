from typing import List, Tuple
from board_lists import *
import random

RED = "\033[31m"
RESET = "\033[0m"


class Board:
    """
    A class to represent a state a board.

    ...

    Attributes
    ----------
    board : list
        the content of the board
    start : (int, int)
        the starting coordinates
    goal : (int, int)
        the goal coordinates
    visited : list
        array to keep track of the visited positions
    visited_shapes : set
        set to keep track of visited shapes
    all_shapes : set
        set to keep track of all shapes
    size : int
        board size

    Methods
    -------
    reset
    visit
    unvisit
    """

    ACTIONS = [
        (1, 0),  # DOWN
        (0, 1),  # RIGHT
        (-1, 0),  # UP
        (0, -1),  # LEFT
    ]

    def __init__(self, difficulty: int) -> None:
        self.board = choose_random_board(difficulty)
        size = len(self.board)
        self.start = (size - 1, 0)
        self.goal = (0, size - 1)
        self.visited = [[0 for _ in range(size)] for _ in range(size)]
        self.visited_shapes = set()
        self.all_shapes = determine_shapes(self.board)
        self.size = size
        self.visit(self.start)

    def reset(self):
        self.visited = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.visited_shapes = set()

    def visit(self, pos) -> None:
        self.visited_shapes.add(self.board[pos[0]][pos[1]])
        self.visited[pos[0]][pos[1]] = 1

    def unvisit(self, pos) -> None:
        shape = self.board[pos[0]][pos[1]]
        if shape != 0:
            self.visited_shapes.discard(shape)
        self.visited[pos[0]][pos[1]] = 0

    # TODO
    def evaluate_board_state(self) -> float:
        return 0.0

    def get_available_actions(self) -> List[Tuple[int, int]]:
        return [(0, 0)]

    def __repr__(self) -> str:
        print(self.size)
        padding_left = 3
        padding_right = 2
        padding_top = "  _" + self.size * "____"
        padding_bot = "  ‾" + self.size * "‾‾‾‾"
        number_space = "   "
        if len(self.all_shapes) >= 10:
            padding_left += 1
            padding_right += 1
            padding_top += self.size * "_"
            padding_bot += self.size * "‾"
            number_space = "    "

        final = "\n "
        for i in range(self.size):
            final += number_space + str(i)
        final += "\n"
        final += padding_top
        final += "\n"
        for line in range(self.size):
            final += str(line) + " "
            for col in range(self.size):
                final += (
                    "|"
                    + RED * self.visited[line][col]
                    + str(self.board[line][col])
                    .rjust(padding_right)
                    .ljust(padding_left)
                    + RESET
                )
            final += "|\n"
        final += padding_bot
        final += "\n"
        return final

    def __str__(self) -> str:
        print(self.size)
        padding_left = 3
        padding_right = 2
        padding_top = "  _" + self.size * "____"
        padding_bot = "  ‾" + self.size * "‾‾‾‾"
        number_space = "   "
        if len(self.all_shapes) >= 10:
            padding_left += 1
            padding_right += 1
            padding_top += self.size * "_"
            padding_bot += self.size * "‾"
            number_space = "    "

        final = "\n "
        for i in range(self.size):
            final += number_space + str(i)
        final += "\n"
        final += padding_top
        final += "\n"
        for line in range(self.size):
            final += str(line) + " "
            for col in range(self.size):
                final += (
                    "|"
                    + RED * self.visited[line][col]
                    + str(self.board[line][col])
                    .rjust(padding_right)
                    .ljust(padding_left)
                    + RESET
                )
            final += "|\n"
        final += padding_bot
        final += "\n"
        return final


def is_complete(pos, goal) -> bool:
    """
    Checks if the board is complete

        Parameters:
            pos (int, int): the current position
            goal (int, int): the final position

        Returns:
            finished (bool): whether the player has reached the final position
    """
    return pos == goal


def visited_all(board: Board) -> bool:
    """
    Checks if the player has visited all the different shapes

        Parameters:
            board (Board): the board's content

        Return:
            visited_all (bool): whether the player has visited all the shapes
    """
    return board.visited_shapes == board.all_shapes


def is_solved(pos, goal, board: Board) -> bool:
    """
    Checks if the game is solved

        Parameters:
            pos (int, int): the current position for the player
            goal (int, int): the coordinates of the final position
            board (Board): the board's content

        Returns:
            is_solved (bool): wheter the game is solved
    """
    return is_complete(pos, goal) and visited_all(board)


def check_bounds(board: Board, pos: list) -> bool:
    """
    Checks if a position is within bounds of the board

        Parameters:
            board (Board): the board
            pos (list): the position

        Returns:
            in_bounds: whether the position is within bounds
    """
    return not (
        pos[0] < 0 or pos[1] < 0 or pos[0] >= board.size or pos[1] >= board.size
    )


def check_valid(board: Board, pos) -> bool:
    """
    Checks if a play is valid

        Parameters:
            board (Board): the board
            pos (list): current position on the algorithm, on the maze

        Returns:
            is_valid (bool): whether the play in valid
    """

    if not check_bounds(board, pos):
        return False

    shape = board.board[pos[0]][pos[1]]

    if board.visited[pos[0]][pos[1]] == 1:
        return False

    if shape in board.visited_shapes and shape != 0:
        return False

    return True


def determine_shapes(board: list[list[int]]) -> set:
    """
    Determines shapes from board content

        Parameters:
            board (list[list[int]]): the content of the board

        Returns:
            shapes (set): the set of different shapes in the board
    """
    final = set()
    for line in board:
        for num in line:
            if num not in final:
                final.add(num)
    return final


def generate_board(difficulty: int) -> Board:
    """
    Generates a board with a given difficulty

        Parameters:
            difficulty (int): the desired game difficulty

        Returns:
            board (Board): a board with the desired difficulty
    """
    return Board(difficulty)


def choose_random_board(difficulty: int) -> list[list[int]]:
    """
    Chooses a board randomly from a set of boards of a given difficulty

        Parameters:
            difficulty (int): the difficulty level

        Returns:
            board (list[list[int]]): the content of the board
    """
    if difficulty == 1:
        return random.choice(EASY_BOARDS_LIST)
    elif difficulty == 2:
        return random.choice(MEDIUM_BOARDS_LIST)
    elif difficulty == 3:
        return random.choice(HARD_BOARDS_LIST)
    elif difficulty == 4:
        return random.choice(EXTREME_BOARDS_LIST)
    else:
        return [[-1]]
