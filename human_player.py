"""
Human player module.

This module contains the HumanPlayer class, which represents a human player interacting via input.
"""

from player import Player

class HumanPlayer(Player):
    """
    A human player that provides moves based on input (e.g., mouse clicks).

    Attributes
    ----------
    symbol : str
        The symbol representing the player ('X' or 'O').
    """

    def __init__(self, symbol: str):
        """
        Initialize the HumanPlayer.

        :param symbol: The symbol representing the player ('X' or 'O').
        """
        super().__init__(symbol)

    def get_move(self, pos: tuple[int, int], square_size: int) -> tuple[int, int]:
        """
        Get the next move from the human player based on input position.

        :param pos: Tuple (x, y) representing the input position (e.g., mouse click).
        :param square_size: Size of each square on the board.
        :return: Tuple (row, col) representing the move.
        """
        x, y = pos
        row = y // square_size
        col = x // square_size
        return row, col


