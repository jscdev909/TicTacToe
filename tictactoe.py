import random

def display_board(game_board: list[list[str]]):
    print("   " + "   ".join(str(i) for i in range(len(game_board))))
    for i, board_row in enumerate(game_board):
        print(f"{str(i)} " + "|".join(f" {char} " if char else "   " for char in board_row))
        if i != len(game_board) - 1:
            print("  -----------")


def board_full(game_board: list[list[str]]) -> bool:
    return all("" not in board_row for board_row in game_board)


def get_next_cpu_move(game_board: list[list[str]], player_token: str, cpu_token: str) -> tuple[int, int]:
    """
    Used by the CPU to determine the best move it can make at any given time

    The types of moves the CPU can make are categorized into the following types,
    which are prioritized in the order listed, highest priority descending:

    - Winning moves are moves that will immediately win the game for the CPU
    - Blocking moves are moves that block the player from winning during their next turn
    - Advancing moves are moves that advance the CPU closer to winning
    - Random moves are all other moves which don't fall into one of the above categories

    A winning move, when found, is returned immediately. As long as no winning moves
    are found, other types of moves (blocking, advancing, random) will be collected.
    If blocking moves are found by the end of the function, one will be randomly selected
    and returned. If no blocking moves are found, and advancing moves have been found,
    an advancing move will be randomly selected and returned. If no blocking moves or
    advancing moves have been found, a random move will be randomly selected and returned.
    """

    blocking_moves = []
    advancing_moves = []
    random_moves = []

    checks = []

    available_spaces = [(r, c) for r in range(3) for c in range(3) if not game_board[r][c]]

    for space in available_spaces:
        match space:
            case (0, 0):
                checks = [[game_board[0][0], game_board[1][0], game_board[2][0]],
                          [game_board[0][0], game_board[0][1], game_board[0][2]],
                          [game_board[0][0], game_board[1][1], game_board[2][2]]]
            case (0, 1):
                checks = [[game_board[0][0], game_board[0][1], game_board[0][2]],
                          [game_board[0][1], game_board[1][1], game_board[2][1]]]

            case (0, 2):
                checks = [[game_board[0][0], game_board[0][1], game_board[0][2]],
                          [game_board[0][2], game_board[1][2], game_board[2][2]],
                          [game_board[2][0], game_board[1][1], game_board[0][2]]]
            case (1, 0):
                checks = [[game_board[0][0], game_board[1][0], game_board[2][0]],
                          [game_board[1][0], game_board[1][1], game_board[1][2]]]

            case (1, 1):
                checks = [[game_board[0][0], game_board[1][1], game_board[2][2]],
                          [game_board[2][0], game_board[1][1], game_board[0][2]],
                          [game_board[0][1], game_board[1][1], game_board[2][1]],
                          [game_board[1][0], game_board[1][1], game_board[1][2]]]

            case (1, 2):
                checks = [[game_board[0][2], game_board[1][2], game_board[2][2]],
                          [game_board[1][0], game_board[1][1], game_board[1][2]]]

            case (2, 0):
                checks = [[game_board[0][0], game_board[1][0], game_board[2][0]],
                          [game_board[2][0], game_board[1][1], game_board[0][2]],
                          [game_board[2][0], game_board[2][1], game_board[2][2]]]
            case (2, 1):
                checks = [[game_board[2][0], game_board[2][1], game_board[2][2]],
                          [game_board[0][1], game_board[1][1], game_board[2][1]]]

            case (2, 2):
                checks = [[game_board[0][0], game_board[1][1], game_board[2][2]],
                          [game_board[2][0], game_board[2][1], game_board[2][2]],
                          [game_board[0][2], game_board[1][2], game_board[2][2]]]

        advancing_count = 0
        blocking_count = 0
        for check in checks:
            player_count = check.count(player_token)
            cpu_count = check.count(cpu_token)
            if cpu_count == 2:
                # Found a winning move
                return space
            elif player_count == 2:
                blocking_count += 1
            elif cpu_count == 1 and player_count == 0:
                advancing_count += 1

        if blocking_count > 0:
            blocking_moves.append(space)
        elif advancing_count > 0:
            advancing_moves.append(space)
        else:
            random_moves.append(space)

    if blocking_moves:
        return random.choice(blocking_moves)
    elif advancing_moves:
        return random.choice(advancing_moves)
    else:
        return random.choice(random_moves)


def check_for_win(game_board: list[list[str]], player_token: str, cpu_token: str) -> tuple[bool, None | str]:
    # Check rows
    for i in range(3):
        row_as_set = set(game_board[i])
        if len(row_as_set) == 1 and ("X" in row_as_set or "O" in row_as_set):
            if player_token in row_as_set:
                return True, player_token
            else:
                return True, cpu_token

    # Check columns
    for i in range(3):
        column_as_set = {game_board[0][i], game_board[1][i], game_board[2][i]}
        if len(column_as_set) == 1 and ("X" in column_as_set or "O" in column_as_set):
            if player_token in column_as_set:
                return True, player_token
            else:
                return True, cpu_token

    # Check diagonals
    diagonal1_as_set = {game_board[0][0], game_board[1][1], game_board[2][2]}
    diagonal2_as_set = {game_board[2][0], game_board[1][1], game_board[0][2]}
    if ((len(diagonal1_as_set) == 1 and ("X" in diagonal1_as_set or "O" in diagonal1_as_set)) or
        (len(diagonal2_as_set) == 1 and ("X" in diagonal2_as_set or "O" in diagonal2_as_set))):

        # Position (1, 1) is shared between both diagonals so check that space for the winning token
        if game_board[1][1] == player_token:
            return True, player_token
        else:
            return True, cpu_token

    return False, None


print("Welcome to Tic-Tac-Toe!")

player_char = ""
while player_char not in ["X", "O"]:
    player_char = input("X or O? [X/O]: ")

cpu_char = "X" if player_char == "O" else "O"

user_input = ""
while user_input != "n":

    board = [["", "", ""], ["", "", ""], ["", "", ""]]

    while not board_full(board) and not check_for_win(board, player_char, cpu_char)[0]:

        display_board(board)

        row = ""
        while not row.isdigit() or not (0 <= int(row) <= 2):
            row = input("Enter a row number [0-2]: ")
        row = int(row)
        col = ""
        while not col.isdigit() or not (0 <= int(col) <= 2):
            col = input("Enter a column number [0-2]: ")
        col = int(col)

        if board[row][col] in ["X", "O"]:
            print(f"Position ({row}, {col}) is already taken!")
            continue

        board[row][col] = player_char

        if board_full(board) or check_for_win(board, player_char, cpu_char)[0]:
            break

        cpu_choice = get_next_cpu_move(board, player_char, cpu_char)
        board[cpu_choice[0]][cpu_choice[1]] = cpu_char

    display_board(board)

    win_check = check_for_win(board, player_char, cpu_char)

    if win_check[0]:
        if player_char == win_check[1]:
            print("You win!")
        else:
            print("Sorry, you lose!")
    elif board_full(board):
        print("Tie game, board is full!")

    user_input = ""
    while user_input not in ["y", "n"]:
        user_input = input("Would you like to play again? [y/n]: ")

print("Thanks for playing!")