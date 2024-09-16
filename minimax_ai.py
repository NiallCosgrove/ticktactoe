"""
Minimax AI player module.

This module contains the MinimaxAI class, which represents an AI player that uses the Minimax algorithm
with alpha-beta pruning and iterative deepening.
"""

from player import Player
import numpy as np
import math
import time
import logging
from numba import njit

class MinimaxAI(Player):
    """
    An AI player that uses the Minimax algorithm with alpha-beta pruning and iterative deepening.

    Attributes
    ----------
    symbol : str
        The symbol representing the player ('X' or 'O').
    max_depth : int, optional
        Maximum depth for the Minimax search (None for unlimited).
    time_limit : float, optional
        Time limit in seconds for iterative deepening.
    name : str
        Identifier name for the AI instance (useful for logging and debugging).
    """

    def __init__(self, symbol: str, max_depth: int = None, time_limit: float = None, name: str = 'AI'):
        """
        Initialize the Minimax AI player with iterative deepening and advanced reporting.

        :param symbol: The symbol representing the player ('X' or 'O').
        :param max_depth: Maximum depth for the Minimax search (None for unlimited).
        :param time_limit: Time limit in seconds for iterative deepening.
        :param name: Identifier name for the AI instance (useful for multiple AIs).
        """
        super().__init__(symbol)
        self.max_depth = max_depth  # None means no depth limit
        self.time_limit = time_limit  # Time limit for iterative deepening
        self.symbol_value = 1 if symbol == 'X' else -1
        self.WIN_LENGTH = None  # To be set during get_move
        self.board_size = None   # To be set during get_move
        self.name = name  # Name of the AI instance for logging purposes

        # Configure logging
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.name} - %(message)s', datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_move(self, board: np.ndarray, win_length: int) -> tuple[int, int]:
        """
        Determine the best move using iterative deepening with the Minimax algorithm.

        :param board: 2D NumPy array representing the current board state.
        :param win_length: Number of consecutive symbols needed to win.
        :return: Tuple (row, col) representing the best move.
        """
        self.WIN_LENGTH = win_length
        self.board_size = board.shape[0]
        self.transposition_table = {}  # Clear the transposition table
        self.nodes_searched = 0  # Reset node counter
        self.max_depth_reached = 0  # Initialize max depth

        start_time = time.time()
        time_limit = self.time_limit if self.time_limit is not None else float('inf')

        board_copy = board.copy()

        winning_move = self.find_immediate_win(board_copy)
        if winning_move:
            self.nodes_searched += 1
            elapsed_time = int((time.time() - start_time) * 1000)
            pv_moves = f'({winning_move[0]},{winning_move[1]})'
            nps = int(self.nodes_searched / ((elapsed_time / 1000) or 1))
            self.logger.info(
                f"info depth 1 score 10000 nodes {self.nodes_searched} time {elapsed_time} nps {nps} pv {pv_moves}")
            return winning_move

        blocking_move = self.find_immediate_block(board_copy)
        if blocking_move:
            self.nodes_searched += 1
            elapsed_time = int((time.time() - start_time) * 1000)
            pv_moves = f'({blocking_move[0]},{blocking_move[1]})'
            nps = int(self.nodes_searched / ((elapsed_time / 1000) or 1))
            self.logger.info(
                f"info depth 1 score -10000 nodes {self.nodes_searched} time {elapsed_time} nps {nps} pv {pv_moves}")
            return blocking_move

        best_score = -math.inf
        best_move = None
        pv_sequence = []
        total_nodes_searched = 0

        depth = 1
        while True:
            current_time = time.time()
            if current_time - start_time >= time_limit:
                break
            if self.max_depth is not None and depth > self.max_depth:
                break

            self.nodes_searched = 0
            self.transposition_table.clear()

            possible_moves = self.get_possible_moves(board_copy)
            ordered_moves = sorted(
                possible_moves, key=lambda move: self.evaluate_move(board_copy, move), reverse=True)

            current_best_score = -math.inf
            current_best_move = None
            current_pv_sequence = []

            try:
                for move in ordered_moves:
                    row, col = move
                    board_copy[row, col] = self.symbol_value
                    eval_score, pv = self.minimax(
                        board_copy, depth=1, max_depth=depth, is_maximizing=False,
                        alpha=-math.inf, beta=math.inf, start_time=start_time, time_limit=time_limit)
                    board_copy[row, col] = 0
                    if eval_score > current_best_score:
                        current_best_score = eval_score
                        current_best_move = move
                        current_pv_sequence = [move] + pv
                    if time.time() - start_time >= time_limit:
                        raise TimeoutError
                if current_best_move is not None:
                    best_score = current_best_score
                    best_move = current_best_move
                    pv_sequence = current_pv_sequence
                    self.max_depth_reached = depth
            except TimeoutError:
                break

            total_nodes_searched += self.nodes_searched

            elapsed_time = int((time.time() - start_time) * 1000)
            nps = int(total_nodes_searched / ((elapsed_time / 1000) or 1))
            pv_moves = ' '.join([f'({r},{c})' for r, c in pv_sequence])
            self.logger.info(
                f"info depth {depth} score {best_score} nodes {total_nodes_searched} time {elapsed_time} nps {nps} pv {pv_moves}")

            depth += 1

            if time.time() - start_time >= time_limit:
                break
            if self.max_depth is not None and depth > self.max_depth:
                break

        return best_move

    def minimax(self, board: np.ndarray, depth: int, max_depth: int, is_maximizing: bool,
                alpha: float, beta: float, start_time: float, time_limit: float) -> tuple[int, list]:
        """
        Recursive Minimax algorithm with alpha-beta pruning and transposition tables.

        :param board: 2D NumPy array representing the current board state.
        :param depth: Current depth in the game tree.
        :param max_depth: Maximum depth to search in this iteration.
        :param is_maximizing: Boolean indicating if the current layer is maximizing.
        :param alpha: Alpha value for pruning.
        :param beta: Beta value for pruning.
        :param start_time: Start time of the move computation.
        :param time_limit: Time limit in seconds for the entire move computation.
        :return: Tuple (score, pv_sequence).
        """
        if time.time() - start_time >= time_limit:
            raise TimeoutError

        self.nodes_searched += 1

        winner = self.check_winner(board)
        if winner != 0:
            score = 10000 - depth if winner == self.symbol_value else -10000 + depth
            return score, []

        if depth >= max_depth:
            score = self.evaluate_board(board)
            return score, []

        if self.is_draw(board):
            return 0, []

        board_key = self.board_to_key(board)
        if board_key in self.transposition_table:
            return self.transposition_table[board_key]

        possible_moves = self.get_possible_moves(board)
        ordered_moves = sorted(
            possible_moves, key=lambda move: self.evaluate_move(board, move), reverse=is_maximizing)

        if is_maximizing:
            max_eval = -math.inf
            best_pv = []
            for move in ordered_moves:
                if time.time() - start_time >= time_limit:
                    raise TimeoutError
                row, col = move
                board[row, col] = self.symbol_value
                eval_score, pv = self.minimax(
                    board, depth + 1, max_depth, False, alpha, beta, start_time, time_limit)
                board[row, col] = 0
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_pv = [move] + pv
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = (max_eval, best_pv)
            return max_eval, best_pv
        else:
            min_eval = math.inf
            best_pv = []
            opponent_value = -self.symbol_value
            for move in ordered_moves:
                if time.time() - start_time >= time_limit:
                    raise TimeoutError
                row, col = move
                board[row, col] = opponent_value
                eval_score, pv = self.minimax(
                    board, depth + 1, max_depth, True, alpha, beta, start_time, time_limit)
                board[row, col] = 0
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_pv = [move] + pv
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = (min_eval, best_pv)
            return min_eval, best_pv

    def find_immediate_win(self, board: np.ndarray) -> tuple[int, int] or None:
        """
        Check for any immediate winning move for the AI.

        :param board: 2D NumPy array representing the current board state.
        :return: Tuple (row, col) if a winning move is found, else None.
        """
        possible_moves = self.get_possible_moves(board)
        for move in possible_moves:
            row, col = move
            board[row, col] = self.symbol_value
            if self.check_winner(board) == self.symbol_value:
                board[row, col] = 0
                return move
            board[row, col] = 0
        return None

    def find_immediate_block(self, board: np.ndarray) -> tuple[int, int] or None:
        """
        Check for any immediate winning move for the opponent and block it.

        :param board: 2D NumPy array representing the current board state.
        :return: Tuple (row, col) if a blocking move is found, else None.
        """
        opponent_value = -self.symbol_value
        possible_moves = self.get_possible_moves(board)
        for move in possible_moves:
            row, col = move
            board[row, col] = opponent_value
            if self.check_winner(board) == opponent_value:
                board[row, col] = 0
                return move
            board[row, col] = 0
        return None

    def get_possible_moves(self, board: np.ndarray) -> list[tuple[int, int]]:
        """
        Generate all possible moves (empty squares) on the board.

        :param board: 2D NumPy array representing the current board state.
        :return: List of tuples (row, col) indicating possible moves.
        """
        return list(zip(*np.where(board == 0)))

    def evaluate_move(self, board: np.ndarray, move: tuple[int, int]) -> int:
        """
        Heuristic evaluation of a move to assist in move ordering.

        :param board: 2D NumPy array representing the current board state.
        :param move: Tuple (row, col) representing the move to evaluate.
        :return: Heuristic score for the move.
        """
        row, col = move
        center = self.board_size // 2
        score = (self.board_size - (abs(row - center) + abs(col - center)))

        board[row, col] = self.symbol_value
        if self.check_winner(board) == self.symbol_value:
            score += 1000
        board[row, col] = 0

        opponent_value = -self.symbol_value
        board[row, col] = opponent_value
        if self.check_winner(board) == opponent_value:
            score += 500
        board[row, col] = 0

        return score

    def evaluate_board(self, board: np.ndarray) -> int:
        """
        Evaluate the board from the perspective of the AI.

        :param board: 2D NumPy array representing the current board state.
        :return: Heuristic score of the board.
        """
        score = 0

        lines = self.get_all_lines(board)
        for line in lines:
            score += self.evaluate_line(line)

        return score

    def get_all_lines(self, board: np.ndarray) -> list[list[int]]:
        """
        Extract all possible lines (rows, columns, diagonals) from the board.

        :param board: 2D NumPy array representing the current board state.
        :return: List of lists, each representing a line.
        """
        lines = []

        lines.extend(board.tolist())

        lines.extend(board.T.tolist())

        lines.extend(self.get_diagonals(board))

        return lines

    def get_diagonals(self, board: np.ndarray) -> list[list[int]]:
        """
        Extract all diagonals of length >= WIN_LENGTH from the board.

        :param board: 2D NumPy array representing the current board state.
        :return: List of lists, each representing a diagonal.
        """
        diagonals = []

        for offset in range(-(self.board_size - self.WIN_LENGTH), self.board_size - self.WIN_LENGTH + 1):
            diag = board.diagonal(offset).tolist()
            if len(diag) >= self.WIN_LENGTH:
                diagonals.append(diag)

        flipped_board = np.flipud(board)
        for offset in range(-(self.board_size - self.WIN_LENGTH), self.board_size - self.WIN_LENGTH + 1):
            diag = flipped_board.diagonal(offset).tolist()
            if len(diag) >= self.WIN_LENGTH:
                diagonals.append(diag)

        return diagonals

    def evaluate_line(self, line: list[int]) -> int:
        """
        Evaluate a single line for heuristic scoring.

        :param line: List representing a line (row, column, or diagonal).
        :return: Heuristic score for the line.
        """
        score = 0
        length = len(line)

        for i in range(length - self.WIN_LENGTH + 1):
            window = line[i:i + self.WIN_LENGTH]
            score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window: list[int]) -> int:
        """
        Evaluate a window of WIN_LENGTH cells.

        :param window: List representing a window of the line.
        :return: Heuristic score for the window.
        """
        score = 0
        my_count = window.count(self.symbol_value)
        opp_count = window.count(-self.symbol_value)

        if my_count > 0 and opp_count == 0:
            score += self.line_score(my_count)
        elif opp_count > 0 and my_count == 0:
            score -= self.line_score(opp_count)

        return score

    def line_score(self, count: int) -> int:
        """
        Assign a score based on the number of symbols in a line.

        :param count: Number of symbols.
        :return: Heuristic score.
        """
        if count == self.WIN_LENGTH:
            return 10000
        elif count == self.WIN_LENGTH - 1:
            return 1000
        elif count == self.WIN_LENGTH - 2:
            return 100
        elif count == self.WIN_LENGTH - 3:
            return 10
        else:
            return 1

    def check_winner(self, board: np.ndarray) -> int:
        """
        Check if there is a winner on the board.

        :param board: 2D NumPy array representing the current board state.
        :return: 1 if Player X wins, -1 if Player O wins, 0 otherwise.
        """
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                symbol = board[row, col]
                if symbol != 0:
                    for dx, dy in directions:
                        if self.check_direction(
                            board, row, col, dx, dy, symbol, self.WIN_LENGTH):
                            return symbol
        return 0

    @staticmethod
    @njit
    def check_direction(board: np.ndarray, row: int, col: int, dx: int, dy: int,
                        symbol: int, win_length: int) -> bool:
        """
        Check a specific direction for a win. Optimized with Numba.

        :param board: 2D NumPy array representing the current board state.
        :param row: Starting row index.
        :param col: Starting column index.
        :param dx: Direction step for rows.
        :param dy: Direction step for columns.
        :param symbol: Player symbol to check.
        :param win_length: Number of consecutive symbols needed to win.
        :return: True if a win is found in the specified direction, False otherwise.
        """
        for _ in range(1, win_length):
            row += dx
            col += dy
            if row < 0 or row >= board.shape[0] or col < 0 or col >= board.shape[1]:
                return False
            if board[row, col] != symbol:
                return False
        return True

    def board_to_key(self, board: np.ndarray) -> bytes:
        """
        Convert the board to a hashable key for transposition table.

        :param board: 2D NumPy array representing the current board state.
        :return: Bytes representing the board state.
        """
        return board.tobytes()

    def is_draw(self, board: np.ndarray) -> bool:
        """
        Check if the game is a draw.

        :param board: 2D NumPy array representing the current board state.
        :return: True if the game is a draw, False otherwise.
        """
        return not np.any(board == 0)
