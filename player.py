"""
Player base class module.

This module defines the base Player class to be inherited by specific player implementations.
"""

class Player:
    """
    Base class for a player in the Tic-Tac-Toe game.
    """
    def __init__(self, symbol):
        """
        Initialize the player with a symbol.

        :param symbol: The symbol representing the player ('X' or 'O').
        """
        self.symbol = symbol

    def get_move(self, board, square_size):
        """
        Get the next move for the player.

        :param board: 2D list representing the game board.
        :param square_size: Size of each square on the board (unused in base class).
        :return: Tuple (row, col) representing the move.
        """
        # This method should be implemented by subclasses
        raise NotImplementedError("Subclasses must implement this method.")

