# goal: build pass and play connect four in terminal

START_BOARD = ".........................................."
# step one: print board from board string
valid_boards = [
    "..........................................",
    "........................................RY",
    ".................................RY.....RY",
]

diag_left_wins = [
".................R......RR.....YYR...YRYYR"
]

def printBoard(board):
    """Takes board string and prints a board to terminal."""

    boardArray = []
    i = 0
    while i < len(board):
        
        row = []
        j = 0
        while j < 7:
            row.append(board[i])
            j+=1
            i+=1
        boardArray.append(row)
        j = 0
    
    for row in boardArray:
        print("".join(row))


def createBoardArray(board):
    boardArray = []
    i = 0
    while i < len(board):
        
        row = []
        j = 0
        while j < 7:
            row.append(board[i])
            j+=1
            i+=1
        boardArray.append(row)
        j = 0
    
    return boardArray

def dropPiece(board: str, player_choice, player_color) -> bool:
    """Update the board according to the player's choice."""

    # check player_choice - 1 column for first empty position, then update it
    boardArray = createBoardArray(board)
    
    new_board = ""
    for row in reversed(boardArray):
        if row[player_choice - 1] == '.':
            row[player_choice - 1] = player_color
            for row in boardArray:
                for c in row:
                    new_board = new_board + c
            return new_board
    
    # if we make it here, the column was full
    return new_board

def checkDiagLeft(board, r, c, color, count):
    """Check if piece diag left up is correct color, increment count."""
    if count == 4:
        return True
    
    if board[r][c] == color:
        count+=1
        return checkDiagLeft(board, r-1,c-1, color, count)
    else:
        return False

def checkDiagRight(board, r, c, color, count):
    """Check if piece diag right up is correct color, increment count."""
    if count == 4:
        return True
    
    if board[r][c] == color:
        count+=1
        return checkDiagRight(board, r-1, c+1, color, count)
    else:
        return False
    

def isWinning(board):
    """If board is winning, return True and the color of the winning side."""

    # horizontal case
    boardArray = createBoardArray(board)

    for row in boardArray:

        count = 0
        prev = None
        for piece in row:
            if piece == '.':
                count = 0
                prev = None
                continue
            
            # start sequence
            if count == 0 and (piece == 'R' or piece == 'Y'):
                count = 1
                prev = piece
                continue

            if piece == prev:
                count+=1
            else:
                count = 1
                prev = piece
            
            if count == 4:
                return True, piece

    # vertical case
    for c in range(7):

        count = 0
        prev = None
        for row in boardArray:
            piece = row[c]
            if piece == '.':
                count = 0
                prev = None
                continue
            
            # start sequence
            if count == 0 and (piece == 'R' or piece == 'Y'):
                count = 1
                prev = piece
                continue

            if piece == prev:
                count+=1
            else:
                count = 1
                prev = piece
            
            if count == 4:
                return True, piece
    
    # diagonal left case
    diag_left = [(-1,-1)]
    # idea: recursively check neighbors incrementing count
    # only check columns 3-7
    # only check rows 3-6

    for i, row in enumerate(boardArray[3:]):
        for j, col in enumerate(row[3:]):
            color = col
            if color == 'R' or color == 'Y':
                count = 1
                if checkDiagLeft(boardArray, i+3-1, j+3-1, color, count):
                    return True, color

    # diagonal right case
    diag_right = [(-1,1), (1,-1)]
    # idea: recursively check neighbors incrementing count
    # only check columns 0-4
    # only check rows 3-6

    for i, row in enumerate(boardArray[3:]):
        for j, col in enumerate(row[:5]):
            color = col
            if color == 'R' or color == 'Y':
                count = 1
                if checkDiagRight(boardArray, i+3-1, j+1, color, count):
                    return True, color
        
    return False


def playGame():
    """Initiates the game and continues until a winner is found."""

    board = START_BOARD
    # print initial board
    printBoard(board)

    turn_color = 'R'
    while not isWinning(board):
        # get player input
        player_choice = int(input('Select a column (1-7) to drop your piece in: '))

        # get new board
        new_board = dropPiece(board, player_choice, turn_color)
        if not new_board:
            player_choice = input('Column already full! Please select another: ')
            while not dropPiece(board, player_choice, turn_color):
                player_choice = input('Column already full! Please select another: ')

        # print new board
        printBoard(new_board)

        # set board to the new board
        board = new_board

        # change colors
        if turn_color == 'R':
            turn_color = 'Y'
        else:
            turn_color = 'R'
    
    isWin, color = isWinning(board)
    print(f'4 in a row! {color} wins the game!')

playGame()

# sequence:
# while not isWinning(board):
#   red turn: take input from red = choice 0-6
#       for corresponding column, update the empty row with the highest index (bottom to top)
#       print updated board
#   yellow turn: take input from yellow = choice 0-6
#       for corresponding column, update the empty row with the highest index (bottom to top)
#       print updated board
# return the color if board isWinning
