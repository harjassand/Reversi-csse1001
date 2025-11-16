# DO NOT modify or add any import statements
from support import *

# Name: HARJAS SANDHU
# Student Number: 49601040
# Favorite Marsupial: TASMANIAN DEVIL :>
# -----------------------------------------------------------------------------

# Define your functions here (start with def num_hours() -> float)

def num_hours() -> float:
    """
    Returns the number of hours spent on assignment 1 as a float.
    """
    return 51

def move_to_index(move: str) -> tuple[int,int]:
    """
    Returns a tuple (row_index, column_index) to represent the players position on the board.

    Preconditions:
    <move> will be well-formed.
    The first letter of move will be a single capital letter between A and Z inclusive.
    The following integer will be at least 1

    >>> move_to_index("A1")
    (0, 0)

    >>> move_to_index("J3")
    (9, 2)

    >>> move_to_index("D16")
    (3, 15)
    """

    row_letter = move[0]
    column_num = move[1:]

    row_index = ord(row_letter) - ord('A')
    column_index = int(column_num) - 1

    return row_index, column_index

def generate_empty_board(size: int) -> list[list[str]]:
    """
    Returns an empty square board of '+' symbols as a list of lists of strings. Each row and column will have the
    same length as the given input size.

    Preconditions:
    The <size> will be non-negative.

    >>> generate_empty_board(0)
    []

    >>> generate_empty_board(2)
    [['+','+'],['+','+']]
    """

    empty_board = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(EMPTY)
        empty_board.append(row)
    return empty_board

def generate_initial_board() -> list[list[str]]:
    """
    Returns the initial 8x8 game board as a list of lists of strings in its original standard starting state.

    >>> generate_initial_board()
    [['+', '+', '+', '+', '+', '+', '+', '+'],
    ['+', '+', '+', '+', '+', '+', '+', '+'],
    ['+', '+', '+', '+', '+', '+', '+', '+'],
    ['+', '+', '+', 'O', 'X', '+', '+', '+'],
    ['+', '+', '+', 'X', 'O', '+', '+', '+'],
    ['+', '+', '+', '+', '+', '+', '+', '+'],
    ['+', '+', '+', '+', '+', '+', '+', '+'],
    ['+', '+', '+', '+', '+', '+', '+', '+']]
    """
    initial_board = generate_empty_board(BOARD_SIZE)
    initial_board[3][3] = PLAYER_1
    initial_board[3][4] = PLAYER_2
    initial_board[4][4] = PLAYER_1
    initial_board[4][3] = PLAYER_2
    return initial_board

def check_winner(board: list[list[str]]) -> str:
    """
    Returns the most frequently appeared piece, 'X' or 'O', on the given <board>. If the number of 'X' and 'O'
    pieces are equal, an empty string is returned.

    >>> check_winner([['X','O'], ['X', 'O']])
    ''
    >>> check_winner([['X','X'], ['X', 'O']])
    X
    """

    x_count = 0
    o_count = 0
    for row in board:
        for piece in row:
            if piece == PLAYER_2:
                x_count += 1
            elif piece == PLAYER_1:
                o_count +=1

    if x_count > o_count:
        return PLAYER_2
    elif x_count < o_count:
        return PLAYER_1
    else:
        return ''

def sign(num):
    """
    Returns the sign of the integer inputted.
    Returns 1 if <num> is positive.
    Returns -1 if <num> is negative.
    Returns 0 if <num> is zero.

    Preconditions:
    - <num> is an integer

    >>> sign(5)
    1
    >>> sign(-11)
    -1
    >>> sign(0)
    0
    """

    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0

def get_intermediate_locations(position: tuple[int, int], new_position: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Returns a list of (rows, columns) tuples, that lie directly between the given start <position> and end <position>.
    It excludes the start and end themselves.

    Preconditions:

    - Piece will be either X or O

    >>> get_intermediate_locations((0,0), (0,3))
    [(0,1), (0,2)]

    >>> get_intermediate_locations((0,0), (2,3))
    []
    """

    row, column = position
    new_row, new_column = new_position

    row_diff = new_row - row
    column_diff = new_column - column

    #Returns empty list if new position is not in a valid straight line
    if row_diff != 0 and column_diff != 0 and abs(row_diff) != abs(column_diff):
        return []
    intermediate =[]

    row_step = sign(row_diff)
    column_step = sign(column_diff)

    #Move one step ahead to exclude starting position
    row += row_step
    column += column_step

    #Collects all intermediate positions until new position, excluding new position.
    while (row, column) != (new_row, new_column):
        intermediate.append((row, column))
        row += row_step
        column += column_step

    return intermediate


def display_board(board: list[list[str]]) -> None:
    """
    Displays the current game board in a format with row labels (A, B, C, etc.) and column numbers
    (1, 2, 3, etc.).

    Precondition:
    - board will contain at least one row and one column.
    - board will have no more than 26 rows or 9 columns.
    - Each row of board will contain the same number of columns.

    >>> display_board([['X','O'],['+','+']])
      12
      --
    A|XO|
    B|++|
      --
    """

    row_count = len(board)
    column_count = len(board[0])

    # Print column numbers
    print('  ', end='')
    for number in range(1, column_count + 1):
        print(number, end='')
    print('')

    # Print top boarder
    print('  ' + HORIZONTAL_SEPARATOR * column_count)

    # Print each row with corresponding letter and cell contents
    starting_alphabet = ord('A')
    for row_index in range(row_count):
        print(chr(starting_alphabet + row_index) + VERTICAL_SEPARATOR, end='')
        for items in board[row_index]:
            print(items, end='')
        print(VERTICAL_SEPARATOR)

    # Print bottom boarder
    print('  ' + HORIZONTAL_SEPARATOR * column_count)


def get_valid_command(valid_moves: list[str]) -> str:
    """
    Repeatedly prompts the user until a valid input is entered.

    An input can be valid if any of the following are satisfied:
    - A move from the provided valid_moves list (note:  not case-sensitive)
    - 'H' for help
    - 'Q' to quit
    """

    valid_moves_upper = [move.upper() for move in valid_moves]

    while True:
        move = input(MOVE_PROMPT).upper()

        if move == 'Q' or move == 'H':
            return move

        if move in valid_moves_upper:
            return move

def get_reversed_positions(board: list[list[str]], piece: str, position: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Returns a list of (row, column) positions of opponent pieces that would be flipped if the given <piece> is placed at
    the specified <position>.

    Preconditions:
    - <Position> is an index that exists within board.
    - Each row of <board> will contain the same number of columns.

    >>> board = generate_initial_board()
    >>> get_reversed_positions(board, "X", (0,0))
    []
    >>> get_reversed_positions(board, "O", (4,2))
    [(4, 3)]

    >>> board = [["+","+","+","+","+"],
                 ["+","O","O","O","+"],
                 ["+","X","+","X","+"] ,
                 ["+","X","X","X","+"],
                 ["+","+","+","+","+"]]
    >>> get_reversed_positions(board, "O", (3,0))
    [(2, 1)]
    """

    if piece == PLAYER_1:
        opponent = PLAYER_2
    elif piece == PLAYER_2:
        opponent = PLAYER_1
    else:
        return []

    row, col = position
    num_rows_cols = len(board)
    result = []

    if board[row][col] == piece:
        return []

    # All 8 directions, up, down, left, right, and 4 diagonal
    directions = [(1,0), (-1,0),
                  (0,-1), (0,1),
                  (-1,-1), (-1,1),
                  (1,-1), (1,1)]

    for row_direct,col_direct in directions:
        check_row = row + row_direct
        check_col = col + col_direct
        possible_flip = []

        # Check pieces in this direction while staying on the board to find a valid flip
        while 0 <= check_row < num_rows_cols and 0 <= check_col < num_rows_cols:
            current_piece = board[check_row][check_col]

            if current_piece == opponent:
                # Step through in this direction while staying on the board to find a potential flip sequence
                possible_flip.append((check_row, check_col))
                check_row += row_direct
                check_col += col_direct
            elif current_piece == piece:
                # Found own piece after a valid chain, confirm and collect flips
                if possible_flip:
                    result.extend(possible_flip)
                break
            else:
                # Hit an empty square or invalid pattern, no flips in this direction
                break

    return result

def get_available_moves(board: list[list[str]], player: str) -> list[str]:
    """
    Returns the list of available moves that the given <player> can make in the boards current games state.

    Preconditions:
    - Each row of <board> will contain the same number of columns.

    >>> board = generate_initial_board()
    >>> display_board(board)
      12345678
      --------
    A|++++++++|
    B|++++++++|
    C|++++++++|
    D|+++OX+++|
    E|+++XO+++|
    F|++++++++|
    G|++++++++|
    H|++++++++|
      --------
    >>> get_available_moves(board, "X")
    ['C4', 'D3', 'E6', 'F5']

    >>> board = [
                 ["+","+","+","+","+"],
                 ["+","O","O","O","+"],
                 ["+","X","+","X","+"],
                 ["+","X","X","X","+"],
                 ["+","+","+","+","+"]
    ]
    >>> display_board(board)
      12345
      -----
    A|+++++|
    B|+OOO+|
    C|+X+X+|
    D|+XXX+|
    E|+++++|
      -----
    >>> get_available_moves(board, "O")
    ['D1', 'D5', 'E2', 'E4']
    """
    valid_moves = []
    board_size = len(board)

    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] != EMPTY:
                continue
            reversed_pos = get_reversed_positions(board, player, (row, col))
            if reversed_pos:
                # Converts position to standard string format (e.g., 'B3')
                move_str = chr(ord('A') + row) + str(col + 1)
                valid_moves.append(move_str)
    valid_moves.sort()
    return valid_moves

def make_move(board: list[list[str]], piece: str, move: str) -> None:
    """
    Updates the board by placing a <piece> at the given <move> and flipping any opponent pieces according to the rules.

    Preconditions:
    - <move> is well-formed.
    - <move> is given in uppercase.
    - <move> corresponds to a position that exists on the board.
    - Each row of the <board> will contain the same number of columns.

    >>> board = generate_initial_board()
    >>> display_board(board)
      12345678
      --------
    A|++++++++|
    B|++++++++|
    C|++++++++|
    D|+++OX+++|
    E|+++XO+++|
    F|++++++++|
    G|++++++++|
    H|++++++++|
      --------
    >>> make_move(board, "O", "D3")
    >>> display_board(board)
      12345678
      --------
    A|++++++++|
    B|++++++++|
    C|++++++++|
    D|++OOX+++|
    E|+++XO+++|
    F|++++++++|
    G|++++++++|
    H|++++++++|
      --------

    >>> board = [["+","+","+","+","+"],
                 ["+","O","O","O","+"],
                 ["+","X","+","X","+"],
                 ["+","X","X","X","+"],
                 ["+","+","+","+","+"]]
    >>> display_board(board)

      12345
      -----
    A|+++++|
    B|+OOO+|
    C|+X+X+|
    D|+XXX+|
    E|+++++|
      -----
    >>> make_move(board, "O", "D4")
    >>> display_board(board)
      12345
      -----
    A|+++++|
    B|+OOO+|
    C|+X+O+|
    D|+XXO+|
    E|+++++|
      -----
    """
    row, col = move_to_index(move)

    to_flip = get_reversed_positions(board, piece, (row, col))

    board[row][col] = piece
    # Flip opponent piece found in to_flip.
    for row_index, col_index in to_flip:
        board[row_index][col_index] = piece

def play_game():
    """
    Implements the full game of reversi based on the gameplay instructions.
    """

    print(WELCOME_MESSAGE)
    board = generate_initial_board()
    display_board(board)

    current_player = PLAYER_1
    current_player_num = 1

    other_player = PLAYER_2
    other_player_num = 2
    skip_count = 0

    while True:
        valid_moves = get_available_moves(board, current_player)

        if not valid_moves:
            print('Player', current_player_num, 'to move')
            print('Player', current_player_num, 'has no possible move!')
            skip_count += 1

            if skip_count == 2:
                break

            display_board(board)

            # Swaps players
            temp_piece = current_player
            current_player = other_player
            other_player = temp_piece

            temp_num = current_player_num
            current_player_num = other_player_num
            other_player_num = temp_num


            continue

        skip_count = 0
        print('Player', current_player_num, 'to move')
        print('Possible moves: ' + ','.join(valid_moves))

        command = get_valid_command(valid_moves)

        if command.upper() == 'H':
            print(HELP_MESSAGE)
            display_board(board)
            continue


        elif command.upper() == 'Q':
            # Checks current board state if player terminates game early
            winner = check_winner(board)
            if winner == '':
                print(DRAW_TEXT)
            elif winner == PLAYER_1:
                print('Player 1 Wins!')
            else:
                print('Player 2 Wins!')
            return

        make_move(board, current_player, command.upper())
        display_board(board)

        # swap players
        temp_piece = current_player
        current_player = other_player
        other_player = temp_piece

        temp_num = current_player_num
        current_player_num = other_player_num
        other_player_num = temp_num

    # Checks winner
    winner = check_winner(board)

    if winner == '':
        print(DRAW_TEXT)
    elif winner == PLAYER_1:
        print('Player 1 Wins!')
    else:
        print('Player 2 Wins!')

def main() -> None:
    """
    Runs the whole game of Reversi based of the gameplay instructions.

    Repeats the games until the user chooses to quit.
    """
    while True:
        play_game()
        response = input("Would you like to play again? (y/n): ").strip()
        if response.upper() != 'Y':
            break
if __name__ == "__main__":
    main()

