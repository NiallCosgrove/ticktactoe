#!/usr/bin/env python3
"""
Entry point for playing the Tic-Tac-Toe game.

This script initializes the game engine with specified players and starts the game.
"""

import cProfile
from game_engine import GameEngine
from human_player import HumanPlayer
from minimax_ai import MinimaxAI
from random_ai import RandomAI

if __name__ == "__main__":
    """
    Main entry point for setting up and starting the Tic-Tac-Toe game.
    Initializes players and the game engine with a dynamic grid size.
    """
    # Set up players
    player1 = MinimaxAI('X', max_depth=5, time_limit=2, name='Player X')
    player2 = MinimaxAI('O', max_depth=10, time_limit=4, name='Player O')
    # player2 = HumanPlayer('O')  # Uncomment to play against a human player

    # Initialize game engine with dynamic grid size
    game = GameEngine(player1, player2, size=9, win_length=5)

    # Run the game (with optional profiling)
    # cProfile.run('game.run()', 'profiling_results.prof')
    game.run()


