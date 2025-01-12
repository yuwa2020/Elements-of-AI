#!/usr/local/bin/python3
# solver.py : solve the game
#
# Code by: name IU ID
#
# Based on skeleton code for CSCI-B551
#

import sys
import time
import random
from typing import Union


def parse_board_string_to_grid(board: str, n: int) -> list[list[str]]:
    return [[k for k in board[i:i + n]] for i in range(0, len(board), n)]

def parse_board_grid_to_string(board: list[list[str]]) -> str:
    return "".join("".join(row) for row in board)

def return_empty_positions(board: list[list[str]]) -> list[tuple[int, int]]:
    return [(i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] == '.']

def print_board(board: Union[list[list[str]], str], n: int, m: int):
    """Prints the board in a human readable format.

    Args:
        board (Union[list[list[str]], str]): The board to be printed. 
        n (int): number of rows in the board. 
        m (int): number of columns in the board. 
    """
    if isinstance(board, str):
        assert len(board) == n * m, "Board size does not match n x m"
        board = parse_board_string_to_grid(board, m)
    
    for row in board:

        print("".join(row))



def is_solved(board: list[list[int]], numInRow: int) -> bool:
   
    #directions
    directions = [(0, 1), (1,0), (1, 1), (1, -1)]
    
    #for each element check in valid directions to see if solved
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x':
                for dx, dy in directions:
                    found = True
                    for k in range(numInRow):
                        #next index i, j
                        next_i, next_j = i+k*dx, j+k*dy
                        #checking if in bounds
                        if not (0 <= next_i < len(board) and 0 <= next_j < len(board[0])):
                            found = False
                            break
                        #checking if character matches
                        if board[next_i][next_j] != 'x':
                            found = False
                            break
                    if found:
                        return True
    return False



#higher score the closer we are to making n in a row 
def notQuiteLosing(board, move_tuple, n):

    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dx, dy in directions:
        count = 0

        for direction in (-1, 1):
            next_row, next_col = move_tuple[0] + direction * dx, move_tuple[1] + direction * dy
            while 0 <= next_row < len(board) and 0 <= next_col < len(board[0]):
                if board[next_row][next_col] == 'x':
                    count += 1
                else:
                    break
                next_row += direction * dx
                next_col += direction * dy

        score += count**3  # Reward for being close to forming a line

    return score

#move space around our move the better
def takeUpSpace(board, move_tuple, n):
    # "lonliest" move
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dx, dy in directions:
        empty_count = 0

        # Check in both positive and negative directions
        for direction in (-1, 1):
            next_row, next_col = move_tuple[0] + direction * dx, move_tuple[1] + direction * dy
            
            # Count consecutive empty spaces in the current direction
            while 0 <= next_row < len(board) and 0 <= next_col < len(board[0]):
                if board[next_row][next_col] == '.':
                    empty_count += 1
                else:
                    break
                next_row += direction * dx
                next_col += direction * dy

        score += empty_count 

    return score




def alpha_beta( board:list[list[int]], depth, n, alpha, beta, heuristic, maximizingPlayer: bool, last_move: tuple[int, int])->int:

    if depth == 0 or is_solved(board, n):
        result = heuristic(board, last_move, n)
        print("in basecase")
        print(f"Depth {depth}, Move {last_move}, Heuristic = {result}")
        return result

    empty_positions = return_empty_positions(board)

    if maximizingPlayer:
        print("max")
        max_val = -100
        for pos in empty_positions:
            board[pos[0]][pos[1]] = 'x'
            curr_val = alpha_beta(board, depth-1, n, alpha, beta, heuristic, False, pos)
            
            board[pos[0]][pos[1]] = '.'

            max_val = max(max_val, curr_val)
            alpha = max(alpha, curr_val)
            print("alpha")
            if beta <=alpha:
                break
        return max_val
    

    else:
        min_val = 100
        print("min")
        for pos in empty_positions:
            board[pos[0]][pos[1]] = 'x'
            curr_val = alpha_beta(board, depth-1, n, alpha, beta, heuristic, True, pos)

            board[pos[0]][pos[1]] = '.'

            min_val = min(min_val, curr_val)
            beta = min(beta, curr_val)
            print("beta")
            if beta <= alpha:
                break
        return min_val

def solver(board: str, n: int, m: int, length: int):
    """This function should solve the game and return the new board.

    Args:
        board (str): describes the current board state. It is a string of length n x m.
        n (int): number of rows in the board.
        m (int): number of columns in the board.
        length (int): length of the line to be formed.
    """
    assert set(board) in [{'.', 'x'}, {'.'}, {'x'}], "Invalid characters in board"
    assert len(board) == n * m, "Board size does not match n x m"
    #board = parse_board_string_to_grid(board, n)
    board : list[list[str]] = parse_board_string_to_grid(board, m)

    assert is_solved(board, length) == False, "Board is already solved"

    #board : list[list[str]] = parse_board_string_to_grid(board, m)

    # Currently placing 'x' on the board in a random position.
    # This is just a placeholder, and needs to be replaced by the actual algorithm.
    # The algorithm should return a new board, which is different from the input board.


    #first idea is to find a position where you place an x as close to length as possible without being length
        #- increases chance of opponent taking that spot and losing
    
    #second idea: place an x as far away from other x's as much as possible. 
        #- take up empty space so more likely for opponent to connect lines

    
    empty_positions = return_empty_positions(board)
    best_score = float('-inf')
    best_move = None

    heuristic = notQuiteLosing

    depth = 12

    for pos in empty_positions:
        board[pos[0]][pos[1]] = 'x'
        if is_solved(board, length):
            curr_move_score = float('-inf')
        else:

            curr_move_score = alpha_beta(board, depth -1, n = length, alpha = -100, beta = 100, heuristic = heuristic, maximizingPlayer= False, last_move=pos)

        board[pos[0]][pos[1]] = '.'
        print(f"Move {pos}: Score = {curr_move_score}")


        if curr_move_score > best_score:
            best_score = curr_move_score
            best_move = pos

    if best_move:
        board[best_move[0]][best_move[1]] = 'x'
    else:
        move = random.choice(empty_positions)
        [print("move: ", move[0], move[1])]
        board[move[0]][move[1]] = 'x'

    return board
   


if __name__ == "__main__":
    board_string = sys.argv[1]
    n = int(sys.argv[2])
    m = int(sys.argv[3])
    length = int(sys.argv[4])
    print ("Starting from initial board:\n")
    print_board(board_string, n, m)
    print ("\nDeciding the next step...\n")
    new_board = solver(board_string, n, m, length)
    print ("Here's what we found:\n")
    print_board(new_board, n, m)