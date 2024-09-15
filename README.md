# Tic-Tac-Toe Game Engine

This is a Python implementation of a customizable Tic-Tac-Toe game engine suitable for experiments with machine learning. The game supports variable board sizes and win conditions and can be played by human players or AI agents using different strategies.

## Features

- **Variable Board Size**: Play on boards of any size (e.g., 3x3, 5x5, 9x9).
- **Custom Win Conditions**: Set the number of consecutive symbols needed to win.
- **Human and AI Players**: Play against another human or various AI strategies (Random AI, Minimax AI).
- **Extensible Architecture**: Easily add new AI strategies by extending the `Player` base class.

## Installation

Please refer to the [INSTALL.md](INSTALL.md) file for detailed installation instructions on Linux, Windows/WSL, and macOS.

## Usage

- **Starting the Game**: Run `python play_game.py` to start the game.
- **Player Configuration**: Modify `play_game.py` to change player types (e.g., switch between `HumanPlayer`, `RandomAI`, and `MinimaxAI`).
- **Game Settings**: Adjust the board size and win condition in `play_game.py` by modifying the `size` and `win_length` parameters in the `GameEngine` initialization.

## Files Overview

- `play_game.py`: The entry point to start the game.
- `game_engine.py`: Contains the `GameEngine` class handling the game loop and rendering.
- `player.py`: Defines the base `Player` class.
- `human_player.py`: Implements the `HumanPlayer` class for human interaction.
- `random_ai.py`: Implements the `RandomAI` class for random move selection.
- `minimax_ai.py`: Implements the `MinimaxAI` class using the Minimax algorithm with alpha-beta pruning.

## Requirements

See `requirements.txt` for the list of required Python packages.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for improvements and bug fixes.

## License

GPLv3

