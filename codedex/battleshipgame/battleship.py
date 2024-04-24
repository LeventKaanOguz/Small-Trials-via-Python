"""
Important Note: This is a game for 10x10 with 5 ships of lengths 5, 4, 3, 3, 2.
It is a 2 player game with each player having their own board.
The game is played on the console.
"""

import random

board_size = 10

ships = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2,
}

board1 = [["O" for x in range(board_size)] for y in range(board_size)]

board2 = [["O" for x in range(board_size)] for y in range(board_size)]


def print_board(board) -> None:
    for row in board:
        print(" ".join(row))


def get_coords() -> tuple:
    x = int(input("Enter the x coordinate: "))
    y = int(input("Enter the y coordinate: "))
    return x, y


def get_orientation() -> str:
    orientation = input("Enter the orientation (horizontal or vertical): ")
    return orientation


def test_place_ship(board, x, y, orientation, length) -> bool:
    if x < 0 or x >= board_size or y < 0 or y >= board_size:
        return False
    if orientation == "horizontal":
        if x + length > board_size:
            return False
        for i in range(length):
            if board[y][x + i] == "X":
                return False
    elif orientation == "vertical":
        if y + length > board_size:
            return False
        for i in range(length):
            if board[y + i][x] == "X":
                return False

    return True


def place_ship(board, x, y, orientation, length) -> list:
    if orientation == "horizontal":
        for i in range(length):
            board[y][x + i] = "X"
    elif orientation == "vertical":
        for i in range(length):
            board[y + i][x] = "X"
    return board


def playerboard_setup(board: list[list]) -> list[list]:
    for ship in ships:
        while True:
            print_board(board)
            print("Placing the " + ship + " of length " + str(ships[ship]))
            x, y = get_coords()
            orientation = get_orientation()
            if test_place_ship(board, x, y, orientation, ships[ship]) is False:
                print("Invalid placement, try again!")
                continue
            else:
                board = place_ship(board, x, y, orientation, ships[ship])
                break

    return board


def ishit(board, x, y) -> bool:
    return board[y][x] == "X"


def hiddenbotboard_setup(board, hiddenplayer=[[]], x=-1, y=-1) -> list:
    if x == -1 and y == -1:
        return [["0" for x in range(board_size)] for y in range(board_size)]

    if ishit(board, x, y):
        hiddenplayer[y][x] = "H"
    else:
        hiddenplayer[y][x] = "M"

    return hiddenplayer


def botboard_setup(board) -> list:
    for ship in ships:
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            orientation = random.choice(["horizontal", "vertical"])
            if test_place_ship(board, x, y, orientation, ships[ship]) is False:
                continue
            else:
                board = place_ship(board, x, y, orientation, ships[ship])
                break
    return board


def check_loss(board) -> bool:
    if sum(x.count("H") for x in board) == 17:
        return True
    return False


def game() -> None:
    player1 = playerboard_setup(board1)
    hiddenplayer1 = [["0" for x in range(board_size)] for y in range(board_size)]
    hiddenplayer1 = hiddenbotboard_setup(player1)
    player2 = botboard_setup(board2)
    hiddenplayer2 = [["0" for x in range(board_size)] for y in range(board_size)]
    hiddenplayer2 = hiddenbotboard_setup(player2)
    player_turn = 1
    while True:
        if check_loss(hiddenplayer1):
            print("Player 2 wins!")
            break
        elif check_loss(hiddenplayer2):
            print("Player 1 wins!")
            break
        else:
            if player_turn == 1:
                print("Player 1's turn")
                print_board(hiddenplayer2)
                x, y = get_coords()
                hiddenplayer2 = hiddenbotboard_setup(player2, hiddenplayer2, x, y)
                player_turn = 2
            elif player_turn == 2:
                print("Player 2's turn")
                print_board(hiddenplayer1)
                x, y = random.randint(0, 9), random.randint(0, 9)
                hiddenplayer1 = hiddenbotboard_setup(player1, hiddenplayer1, x, y)
                player_turn = 1

    print("Game Over!")
    print("Player 1's board")
    print_board(player1)
    print("Player 2's board")
    print_board(player2)
    print("Player 1's hidden board")
    print_board(hiddenplayer1)
    print("Player 2's hidden board")
    print_board(hiddenplayer2)
    pick = input("Do you want to play again? (yes or no): ")

    if pick == "yes":
        game()
    else:
        print("Thanks for playing!")
        return None

    print("Thanks for playing!")


game()
