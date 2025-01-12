#!/usr/local/bin/python3
# 
#
# Based on skeleton code for CSCI-B551
import pytest
from solver import solver, parse_board_string_to_grid, return_empty_positions, parse_board_grid_to_string
import random

def is_finish_state(board: list[list[str]], n: int, m: int, length: int = 3) -> bool:
    """Check if the board is in a finish state (has a line of X's).
    
    Args:
        board (list[list[str]]): The game board as a 2D list
        n (int): Number of rows in the board
        m (int): Number of columns in the board
        length (int): Length of line needed to win (default 3)
    
    Returns:
        bool: True if board is in finish state, False otherwise
    """
    
    # Check rows
    for i in range(n):
        for j in range(m - length + 1):
            if all(board[i][j+k] == 'x' for k in range(length)):
                return True
    
    # Check columns
    for i in range(n - length + 1):
        for j in range(m):
            if all(board[i+k][j] == 'x' for k in range(length)):
                return True
    
    # Check diagonals (top-left to bottom-right)
    for i in range(n - length + 1):
        for j in range(m - length + 1):
            if all(board[i+k][j+k] == 'x' for k in range(length)):
                return True
    
    # Check diagonals (top-right to bottom-left)
    for i in range(n - length + 1):
        for j in range(length - 1, m):
            if all(board[i+k][j-k] == 'x' for k in range(length)):
                return True
    
    return False

 
def random_solver(board: str, n: int, m: int, length: int = 3) -> list[list[str]]:
    assert set(board) in [{'.', 'x'}, {'.'}, {'x'}], "Invalid characters in board"
    assert len(board) == n * m, "Board size does not match n x m"
    board : list[list[str]] = parse_board_string_to_grid(board, m)
    
    empty_positions = return_empty_positions(board)
    # pick a random empty position from list of empty positions
    i, j = random.choice(empty_positions)
    board[i][j] = 'x'
    return board


def play_game(board: str, n: int, m: int, length: int = 3, player_first: bool = True) -> bool:
    """plays the game against random_solver agent till the end and returns True if player wins, False otherwise

    Args:
        board (str): start state of the board
        n (int): number of rows in the board
        m (int): number of columns in the board
        length (int, optional): length of the line to be formed. Defaults to 3.
        player_first (bool, optional): if True, player starts first. Defaults to True.

    Returns:
        bool: True if player wins, False otherwise
    """
    player_turn = player_first
    previous_board = board
    
    while True:
        if player_turn:
            board = solver(board, n, m, length)
            if is_finish_state(board, n, m, length):
                return False
        else:
            board = random_solver(board, n, m, length)
            if is_finish_state(board, n, m, length):
                return True
        
        
        player_turn = not player_turn
        board = parse_board_grid_to_string(board)
        assert board != previous_board, "Board should change after each turn"
        previous_board = board


time_ = 3000
@pytest.mark.timeout(time_)
def test_game_random_agent_start_first():
    board = "........."
    assert play_game(board, 3, 3, 3, player_first=True) == True

time_ = 3000
@pytest.mark.timeout(time_)
def test_game_random_agent_start_second():
    #board = "........."
    board = "xx......................."
    assert play_game(board, 5, 5, 3, player_first=False) == True


time_ = 300
@pytest.mark.timeout(time_)
def test_trivial_case():
    simple_case = "x...x.xx."
    correct_board = "x...xxxx."
    board = solver(simple_case, 3, 3, 3)
    board = parse_board_grid_to_string(board)
    assert board == correct_board