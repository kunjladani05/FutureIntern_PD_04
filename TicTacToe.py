import random
from constants import PLACE_FILLED_MESSAGE, TIE_MESSAGE, WELCOME_MESSAGE, COMPUTER_WIN_MESSAGE, COMPUTER_MOVE_MESSAGE, \
    PLAYER_WIN_MESSAGE, WELCOME_MESSAGE_TWOPLAYER, INVALID_CHOICE_MESSAGE

# Player vs Player board
player_board = {
    '1': ' ', '2': ' ', '3': ' ',
    '4': ' ', '5': ' ', '6': ' ',
    '7': ' ', '8': ' ', '9': ' '
}

# Computer vs Player board
computer_board = [' ' for _ in range(10)]

turn = 'X'
count = 0


def displayBoard(board):
    """Displays the Tic Tac Toe board.

    Args:
        board (dict or list): The board to display (player's or computer's).
    """
    if isinstance(board, dict):
        print(board['1'] + " | " + board['2'] + " | " + board['3'])
        print("---------")
        print(board['4'] + " | " + board['5'] + " | " + board['6'])
        print("---------")
        print(board['7'] + " | " + board['8'] + " | " + board['9'])
    else:
        print(board[1] + " | " + board[2] + " | " + board[3])
        print("---------")
        print(board[4] + " | " + board[5] + " | " + board[6])
        print("---------")
        print(board[7] + " | " + board[8] + " | " + board[9])

def playgame():
    """Facilitates the Player vs Player game loop."""
    global turn, count
    for i in range(10):
        displayBoard(player_board)
        print("Your turn, " + turn + ", which place to insert (1 to 9)?")
        move = input()

        if player_board[move] == ' ':
            player_board[move] = turn
            count += 1
        else:
            print("\n" + PLACE_FILLED_MESSAGE + "\n")
            continue

        if count >= 5:
            if check_winner(player_board, turn):
                displayBoard(player_board)
                print(turn + " wins!")
                break

        if count == 9:
            displayBoard(player_board)
            print(TIE_MESSAGE + "\n")
            break

        turn = 'O' if turn == 'X' else 'X'


def check_winner(board, player):
    """Checks if a player has won the game.

    Args:
        board (dict): The current game board.
        player (str): The player's symbol ('X' or 'O').

    Returns:
        bool: True if the player has won, False otherwise.
    """
    win_conditions = [
        ('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9'),  # Rows
        ('1', '4', '7'), ('2', '5', '8'), ('3', '6', '9'),  # Columns
        ('1', '5', '9'), ('3', '5', '7')                    # Diagonals
    ]
    return any(all(board[c] == player for c in condition) for condition in win_conditions)


def insertLetter(letter, pos):
    """Inserts a letter at a specified position on the computer board.

    Args:
        letter (str): The letter to insert ('X' or 'O').
        pos (int): The position on the board to insert the letter.
    """
    computer_board[pos] = letter


def spaceIsFree(pos):
    """Checks if a position on the board is free.

    Args:
        pos (int): The position to check.

    Returns:
        bool: True if the position is free, False otherwise.
    """
    return computer_board[pos] == ' '


def isWinner(bo, le):
    """Checks if a letter has won the game.

    Args:
        bo (list): The current game board.
        le (str): The letter to check for a win ('X' or 'O').

    Returns:
        bool: True if the letter has won, False otherwise.
    """
    return (
        (bo[7] == le and bo[8] == le and bo[9] == le) or
        (bo[4] == le and bo[5] == le and bo[6] == le) or
        (bo[1] == le and bo[2] == le and bo[3] == le) or
        (bo[1] == le and bo[4] == le and bo[7] == le) or
        (bo[2] == le and bo[5] == le and bo[8] == le) or
        (bo[3] == le and bo[6] == le and bo[9] == le) or
        (bo[1] == le and bo[5] == le and bo[9] == le) or
        (bo[3] == le and bo[5] == le and bo[7] == le)
    )


def playerMove():
    """Handles the player's move by checking the validity and updating the board."""
    run = True
    while run:
        move = input("Select a position to place an 'X' (1-9): ")
        try:
            move = int(move)
            if move > 0 and move < 10:
                if spaceIsFree(move):
                    run = False
                    insertLetter('X', move)
                else:
                    print(PLACE_FILLED_MESSAGE)
            else:
                print("Please type a number within the range")
        except ValueError:
            print("Please type a number!")


def compMove():
    """Determines the computer's move based on the current state of the board.

    Returns:
        int: The position for the computer's move.
    """
    possibleMoves = [x for x, letter in enumerate(computer_board) if letter == ' ' and x != 0]
    move = 0

    for let in ['O', 'X']:
        for i in possibleMoves:
            boardCopy = computer_board[:]
            boardCopy[i] = let
            if isWinner(boardCopy, let):
                move = i
                return move

    cornersOpen = [i for i in possibleMoves if i in [1, 3, 7, 9]]
    if cornersOpen:
        move = selectRandom(cornersOpen)
        return move

    if 5 in possibleMoves:
        move = 5
        return move

    edgesOpen = [i for i in possibleMoves if i in [2, 4, 6, 8]]
    if edgesOpen:
        move = selectRandom(edgesOpen)

    return move


def selectRandom(li):
    """Selects a random element from a list.

    Args:
        li (list): The list to select from.

    Returns:
        any: A random element from the list.
    """
    return random.choice(li)


def isBoardFull():
    """Checks if the board is full.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    return ' ' not in computer_board[1:]


def main():
    """Main function to run the computer vs player Tic Tac Toe game."""
    print(WELCOME_MESSAGE)
    displayBoard(computer_board)

    while True:
        if not isWinner(computer_board, 'O'):
            playerMove()
            displayBoard(computer_board)
        else:
            print(COMPUTER_WIN_MESSAGE)
            break

        if not isWinner(computer_board, 'X'):
            move = compMove()
            if move == 0:
                print(TIE_MESSAGE)
                break
            else:
                insertLetter('O', move)
                print(COMPUTER_MOVE_MESSAGE.format(move))
                displayBoard(computer_board)
        else:
            print(PLAYER_WIN_MESSAGE)
            break

# Main game loop
while True:
    print(WELCOME_MESSAGE_TWOPLAYER)
    print("1. Two Player")
    print("2. Computer")
    choice = int(input("Enter Your Choice: "))
    if choice == 1:
        playgame()
        break  # Exit after the two-player game
    elif choice == 2:
        main()
        break  # Exit after the computer game
    else:
        print(INVALID_CHOICE_MESSAGE)
