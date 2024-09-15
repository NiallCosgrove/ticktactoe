#!/usr/bin/env python3
"""
Game engine module for Tic-Tac-Toe.

This module defines the GameEngine class, which handles the game logic, rendering,
and interaction between players (human or AI) for a Tic-Tac-Toe game.
"""

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
    Game engine for Tic-Tac-Toe.

    Handles game initialization, rendering, and the game loop.
    """

    def __init__(self, player1, player2, size=3, win_length=3):
        """
        Initialize the game engine.

        :param player1: The first player (human or AI).
        :param player2: The second player (human or AI).
        :param size: The size of the game board (default is 3x3).
        :param win_length: The number of consecutive symbols needed to win.
        """
        # Ensure square grids by using a single size parameter
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
            pygame.draw.line(
                self.screen, LINE_COLOR,
                (col * square_size, 0),
                (col * square_size, self.HEIGHT),
                LINE_WIDTH
            )
        for row in range(1, self.BOARD_ROWS):
            pygame.draw.line(
                self.screen, LINE_COLOR,
                (0, row * square_size),
                (self.WIDTH, row * square_size),
                LINE_WIDTH
            )

    def make_move(self, row, col, player):
        """
        Make a move on the board for a player.

        :param row: The row index for the move.
        :param col: The column index for the move.
        :param player: The player making the move.
        """
        if self.available_square(row, col):
            # Player 1 (X) is represented by 1, Player 2 (O) by -1
            self.board[row, col] = 1 if player == self.player1 else -1
            self.draw_figures()

    def draw_figures(self):
        """
        Draw the X and O figures on the board.
        """
        square_size = self.WIDTH // self.BOARD_COLS

        large_circle_radius = square_size // 3  # Larger "O"
        larger_cross_width = 30  # Larger "X" line width
        larger_space = 20  # Adjust the space for "X"

        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == -1:
                    pygame.draw.circle(
                        self.screen,
                        CIRCLE_COLOR,
                        (int(col * square_size + square_size // 2),
                         int(row * square_size + square_size // 2)),
                        large_circle_radius,
                        CIRCLE_WIDTH
                    )
                elif self.board[row][col] == 1:
                    pygame.draw.line(
                        self.screen,
                        CROSS_COLOR,
                        (col * square_size + larger_space,
                         row * square_size + square_size - larger_space),
                        (col * square_size + square_size - larger_space,
                         row * square_size + larger_space),
                        larger_cross_width
                    )
                    pygame.draw.line(
                        self.screen,
                        CROSS_COLOR,
                        (col * square_size + larger_space,
                         row * square_size + larger_space),
                        (col * square_size + square_size - larger_space,
                         row * square_size + square_size - larger_space),
                        larger_cross_width
                    )

    def available_square(self, row, col):
        """
        Check if a square is available for a move.

        :param row: The row index of the square.
        :param col: The column index of the square.
        :return: True if the square is empty, False otherwise.
        """
        return self.board[row][col] == 0

    def run(self):
        """
        Run the main game loop.
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

                # Human player moves via mouse click
                if isinstance(self.current_player, HumanPlayer) and not self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        square_size = self.WIDTH // self.BOARD_COLS
                        row, col = self.current_player.get_move(pos, square_size)

                        if self.available_square(row, col):
                            self.make_move(row, col, self.current_player)
                            self.handle_turn_end()

            # AI player moves via separate thread
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

        # Clean up after quitting
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
        Handle the end of a player's turn.
        """
        # Print the current board
        print(self.board)

        # Check if the current player wins
        symbol_value = 1 if self.current_player == self.player1 else -1
        print(f"Checking win for p
