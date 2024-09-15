# Installation Guide

This guide will help you set up the Tic-Tac-Toe game in a virtual environment on Linux, Windows/WSL, and macOS.

## Prerequisites

- Python 3.6 or higher
- `pip` package manager

## General Steps

### 1. Clone the Repository

Open your terminal or command prompt and run the following commands:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Create a Virtual Environment

Set up a virtual environment named `venv`:

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

- **Linux and macOS:**

  ```bash
  source venv/bin/activate
  ```

- **Windows/WSL:**

  ```bash
  venv\Scripts\activate
  ```

### 4. Upgrade `pip`

It is recommended to upgrade `pip` before installing the required packages:

```bash
pip install --upgrade pip
```

### 5. Install Dependencies

Install all the necessary packages using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 6. Run the Game

Start the Tic-Tac-Toe game by running the following command:

```bash
python play_game.py
```

## Platform-Specific Instructions

### Linux

1. Ensure Python 3 and `pip` are installed:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. Install the required Pygame dependencies:

   ```bash
   sudo apt install libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev\ 
   libsdl1.2-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev \
   libfreetype6-dev
   ```

### Windows/WSL

1. Install Python 3 from the [official Python website](https://www.python.org/downloads/).

2. Ensure that `pip` is installed (it is bundled with most Python installations). If not, install it separately.

3. Install Pygame:

   ```bash
   pip install pygame
   ```

### macOS

1. Install Homebrew if it is not already installed:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Python 3:

   ```bash
   brew install python
   ```

3. Install the Pygame dependencies:

   ```bash
   brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
   ```

## Additional Notes

### Deactivating the Virtual Environment

Once you're finished, you can deactivate the virtual environment by running:

```bash
deactivate
```

### Changing Game Settings

You can modify `play_game.py` to adjust settings like board size and player types.

## Troubleshooting

### Import Errors

If you encounter import errors, ensure that your virtual environment is activated and all dependencies are installed.

### Pygame Issues

If you experience issues with Pygame, make sure the necessary system libraries are installed. Refer to the [Pygame documentation](https://www.pygame.org/wiki/GettingStarted) for platform-specific installation instructions.

## License

This project is licensed under the GNU General Public License (GPL).
