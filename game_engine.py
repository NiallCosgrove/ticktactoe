import threading
import pygame
import sys
import numpy as np

from human_player import HumanPlayer
from random_ai import RandomAI

# Initialize pygame
pygame.init()

# Define constants for the game
LINE_WIDTH = 15
LINE_COLOR = (23, 145, 135)
WIN_LINE_COLOR = (255, 0, 0)  # Red for the winning line
BG_COLOR = (28, 170, 156)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
CIRCLE_WIDTH = 15
CROSS_WIDTH = 30
SPACE = 20  # Adjusted for larger symbols

class GameEngine:
    """
    A class to represent the Tic-Tac-Toe game engine.

    Attributes
    ----------
    player1 : HumanPlayer or AI
        The first player of the game.
    player2 : HumanPlayer or AI
        The second player of the game.
    size : int, optional
        The size of the game board (default is 3).
    win_length : int, optional
        The number of consecutive symbols needed to win (default is 3).
    """

    def __init__(self, player1, player2, size=3, win_length=3):
        """
        Initialize the game engine with players, board size, and win condition.

        :param player1: The first player (HumanPlayer or AI).
        :param player2: The second player (HumanPlayer or AI).
        :param size: The size of the board, must be a square (e.g., 3x3).
        :param win_length: The number of consecutive symbols needed to win.
        """
        self.BOARD_ROWS = size
        self.BOARD_COLS = size
        self.WIN_LENGTH = win_length  # Parameterized win condition

        # Initialize the game board and other attributes
        self.player1 = player1
        self.player2 = player2
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS), dtype=int)
        self.WIDTH = 600
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill(BG_COLOR)
        self.game_over = False
        self.current_player = self.player1  # Start with Player 1
        self.ai_thread = None
        self.ai_move_ready = False
        self.ai_move = None
        self.ai_lock = threading.Lock()  # To safely share data between threads
        self.win_coords = []  # To store winning coordinates for drawing the line
        self.quit_game = False  # Flag to control quitting the game
        self.draw_grid()

    def draw_grid(self):
        """
        Draw the game grid on the screen.
        """
        square_size = self.WIDTH // self.BOARD_COLS
        for col in range(1, self.BOARD_COLS):
            pygame.draw.line(self.screen, LINE_COLOR, (col * square_size, 0), (col * square_size, self.HEIGHT), LINE_WIDTH)
        for row in range(1, self.BOARD_ROWS):
            pygame.draw.line(self.screen, LINE_COLOR, (0, row * square_size), (self.WIDTH, row * square_size), LINE_WIDTH)

    def make_move(self, row: int, col: int, player):
        """
        Make a move by placing the current player's symbol on the board.

        :param row: The row where the player wants to place their symbol.
        :param col: The column where the player wants to place their symbol.
        :param player: The player making the move (player1 or player2).
        """
        if self.available_square(row, col):
            self.board[row, col] = 1 if player == self.player1 else -1
            self.draw_figures()

    def draw_figures(self):
        """
        Draw the X or O symbols on the board after a move is made.
        """
        square_size = self.WIDTH // self.BOARD_COLS

        large_circle_radius = square_size // 3  # Larger "O"
        larger_cross_width = 30  # Larger "X" line width
        larger_space = 20  # Adjust the space for "X"

        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == -1:
                    pygame.draw.circle(self.screen, CIRCLE_COLOR,
                                       (int(col * square_size + square_size // 2), int(row * square_size + square_size // 2)),
                                       large_circle_radius, 15)
                elif self.board[row][col] == 1:
                    pygame.draw.line(self.screen, CROSS_COLOR,
                                     (col * square_size + larger_space, row * square_size + square_size - larger_space),
                                     (col * square_size + square_size - larger_space, row * square_size + larger_space),
                                     larger_cross_width)
                    pygame.draw.line(self.screen, CROSS_COLOR,
                                     (col * square_size + larger_space, row * square_size + larger_space),
                                     (col * square_size + square_size - larger_space, row * square_size + square_size - larger_space),
                                     larger_cross_width)

    def available_square(self, row: int, col: int) -> bool:
        """
        Check if the square is available for a move.

        :param row: The row index.
        :param col: The column index.
        :return: True if the square is empty, False otherwise.
        """
        return self.board[row][col] == 0

    def run(self):
        """
        Start the game loop, handling events such as player moves and AI turns.
        """
        self.current_player = self.player1  # Ensure Player 1 starts first

        while not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    if event.key == pygame.K_q:
                        self.quit_game = True
                        break  # Exit the event loop

                if isinstance(self.current_player, HumanPlayer) and not self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        square_size = self.WIDTH // self.BOARD_COLS
                        row, col = self.current_player.get_move(pos, square_size)

                        if self.available_square(row, col):
                            self.make_move(row, col, self.current_player)
                            self.handle_turn_end()

            if not isinstance(self.current_player, HumanPlayer) and not self.game_over and not self.quit_game:
                if not self.ai_move_ready:
                    if self.ai_thread is None or not self.ai_thread.is_alive():
                        self.ai_thread = threading.Thread(target=self.compute_ai_move)
                        self.ai_thread.start()
                else:
                    with self.ai_lock:
                        row, col = self.ai_move
                        if self.available_square(row, col):
                            self.make_move(row, col, self.current_player)
                            self.handle_turn_end()
                        self.ai_move_ready = False  # Reset for the next AI turn

            pygame.display.update()

        if self.ai_thread is not None and self.ai_thread.is_alive():
            self.ai_thread.join()
        pygame.quit()
        sys.exit()

    def compute_ai_move(self):
        """
        Compute the AI's move in a separate thread.
        """
        if not self.quit_game:
            row, col = self.current_player.get_move(self.board, self.WIN_LENGTH)
            with self.ai_lock:
                self.ai_move = (row, col)
                self.ai_move_ready = True

    def handle_turn_end(self):
        """
        Handle the end of the current turn, checking for wins or a draw.
        """
        print(self.board)

        symbol_value = 1 if self.current_player == self.player1 else -1
        print(f"Checking win for player {symbol_value}")

        if self.check_win(self.current_player):
            print(f"Player {symbol_value} wins!")
            self.draw_winning_line(symbol_value)
            pygame.display.set_caption(f"Player {'X' if symbol_value == 1 else 'O'} Wins!")
            self.game_over = True

        elif self.is_draw():
            pygame.display.set_caption("Draw!")
            self.game_over = True

        else:
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def check_win(self, player) -> bool:
        """
        Check if the current player has won the game.

        :param player: The player (player1 or player2) to check.
        :return: True if the player has won, False otherwise.
        """
        symbol_value = 1 if player == self.player1 else -1
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == symbol_value:
                    for dx, dy in directions:
                        if self.check_direction(row, col, dx, dy, symbol_value):
                            self.win_coords = [(row + i * dx, col + i * dy) for i in range(self.WIN_LENGTH)]
                            return True
        return False

    def check_direction(self, row: int, col: int, dx: int, dy: int, symbol_value: int) -> bool:
        """
        Check a specific direction on the board for a winning condition.

        :param row: The starting row.
        :param col: The starting column.
        :param dx: The row direction to check.
        :param dy: The column direction to check.
        :param symbol_value: The symbol to check for (1 for player1, -1 for player2).
        :return: True if a win condition is met, False otherwise.
        """
        for i in range(1, self.WIN_LENGTH):
            new_row = row + dx * i
            new_col = col + dy * i
            if not (0 <= new_row < self.BOARD_ROWS and 0 <= new_col < self.BOARD_COLS):
                return False
            if self.board[new_row][new_col] != symbol_value:
                return False
        return True

    def draw_winning_line(self, symbol: int):
        """
        Draw the winning line on the board once a player wins.

        :param symbol: The symbol representing the winning player (1 for X, -1 for O).
        """
        square_size = self.WIDTH // self.BOARD_COLS
        start_row, start_col = self.win_coords[0]
        end_row, end_col = self.win_coords[-1]
        x_start = start_col * square_size + square_size // 2
        y_start = start_row * square_size + square_size // 2
        x_end = end_col * square_size + square_size // 2
        y_end = end_row * square_size + square_size // 2
        pygame.draw.line(self.screen, WIN_LINE_COLOR, (x_start, y_start), (x_end, y_end), LINE_WIDTH)

    def is_draw(self) -> bool:
        """
        Check if the game is a draw (i.e., no empty squares are left).

        :return: True if the game is a draw, False otherwise.
        """
        return not np.any(self.board == 0)

    def reset(self):
        """
        Reset the game board and other states for a new game.
        """
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS), dtype=int)
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.game_over = False
        self.current_player = self.player1
        pygame.display.set_caption("Player X vs Player O")
