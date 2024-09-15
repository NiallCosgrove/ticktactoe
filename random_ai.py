"""
Random AI player module.

This module contains the RandomAI class, which represents an AI player that makes random moves.
"""

import random
from player import Player

class RandomAI(Player):
    """
    An AI player that selects moves randomly from the available options.
    """
    def __init__(self, symbol):
        """
        Initialize the RandomAI player.

        :param symbol: The symbol representing the player ('X' or 'O').
        """
        super().__init__(symbol)

    def get_move(self, board, _):
        """
        Get the next move for the AI player.

        :param board: 2D list representing the game board.
        :param _: Unused parameter (placeholder for square size or other info).
        :return: Tuple (row, col) representing the move, or None if no moves are available.
        """
        # Collect all available squares (those that are 0, meaning empty)
        available_moves = [
            (row, col)
            for row in range(len(board))
            for col in range(len(board[row]))
            if board[row][col] == 0
        ]

        # Randomly choose one of the available moves
        if available_moves:
            return random.choice(available_moves)
        else:
            return None  # No available moves
