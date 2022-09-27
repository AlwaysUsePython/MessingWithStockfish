from chessdotcom import get_player_game_archives
import pprint
import requests
from stockfish import Stockfish
import chess
import pygame
pygame.init()

stockfish = Stockfish(r'C:\Users\ellio\Downloads\stockfish-11-win\stockfish-11-win\Windows\stockfish_20011801_x64.exe')
printer = pprint.PrettyPrinter()



def get_most_recent_game(username):
    data = get_player_game_archives(username).json
    url = data['archives'][-1]
    games = requests.get(url).json()
    game = games['games'][-4]
    return game['pgn']

username = input("Whose account? ")

game = get_most_recent_game(username)

def get_san(pgnString):
    san = []

    currentTwo = "__"
    currentMove = ""
    addToMove = False
    for letter in pgnString:

        currentTwo += letter
        currentTwo = currentTwo[1:]

        if letter == " " and addToMove == True:
            san.append(currentMove)
            currentMove = ""
            addToMove = False

        elif addToMove:
            currentMove += letter

        else:
            if currentTwo == ". ":
                addToMove = True

    return san

def get_uci(san):
    moves = []
    board = chess.Board()

    for move in san:
        moves.append(board.push_san(move))

    return moves

uci = get_uci(get_san(game))

stockfish.set_position(uci)

### PYGAME STUFFS ###
screen = pygame.display.set_mode((1000, 640))

# nightmare nightmare nightmare nightmare nightmare...
BBishop = pygame.image.load("Chess Images/Black Bishop.png")
BKing = pygame.image.load("Chess Images/Black King.png")
BKnight = pygame.image.load("Chess Images/Black Knight.png")
BPawn = pygame.image.load("Chess Images/Black Pawn.png")
BQueen = pygame.image.load("Chess Images/Black Queen.png")
BRook = pygame.image.load("Chess Images/Black Rook.png")


WBishop = pygame.image.load("Chess Images/White Bishop.png")
WKing = pygame.image.load("Chess Images/White King.png")
WKnight = pygame.image.load("Chess Images/White Knight.png")
WPawn = pygame.image.load("Chess Images/White Pawn.png")
WQueen = pygame.image.load("Chess Images/White Queen.png")
WRook = pygame.image.load("Chess Images/White Rook.png")


# Now we need to resize them ahahahahahAHAHAHAHAHAHAHAHAHAHAHA
BBishop = pygame.transform.scale(BBishop, (80, 80))
BKing = pygame.transform.scale(BKing, (80, 80))
BKnight = pygame.transform.scale(BKnight, (80, 80))
BPawn = pygame.transform.scale(BPawn, (80, 80))
BQueen = pygame.transform.scale(BQueen, (80, 80))
BRook = pygame.transform.scale(BRook, (80, 80))


WBishop = pygame.transform.scale(WBishop, (80, 80))
WKing = pygame.transform.scale(WKing, (80, 80))
WKnight = pygame.transform.scale(WKnight, (80, 80))
WPawn = pygame.transform.scale(WPawn, (80, 80))
WQueen = pygame.transform.scale(WQueen, (80, 80))
WRook = pygame.transform.scale(WRook, (80, 80))
def drawBackground():
    # Colors in the black squares
    screen.fill((76,116,156))

    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(640, 0, 360, 640))
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(715, 158, 210, 110))
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(715, 371, 210, 110))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(720, 163, 200, 100))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(720, 163, 200, 100))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(720, 376, 200, 100))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(640, 0, 5, 640))


    # ignore the janky booleans this just alternates squares
    color = True
    startRow = True
    for r in range(8):
        if startRow:
            color = True
            startRow = False
        else:
            color = False
            startRow = True
        for c in range(8):
            if color:
                color = False
                pygame.draw.rect(screen, (236,236,212), pygame.Rect(r * 80, c * 80, 80, 80))
            else:
                color = True

# This function will draw the pieces on top of the board in the right squares. The input is the board as a string
def drawPieces(board):
    pieceCounter = 0
    for piece in board:
        # calculate the row and col of the square. We can use this to get the coords we want for the image.
        col = pieceCounter % 8
        row = pieceCounter // 8
        if piece == "0" or piece == "E":
            screen.blit(WPawn, (80*col, 80*row))
        elif piece == "1" or piece == "F":
            screen.blit(BPawn, (80*col, 80*row))
        elif piece == "2":
            screen.blit(WKnight, (80*col, 80*row))
        elif piece == "3":
            screen.blit(BKnight, (80*col, 80*row))
        elif piece == "4":
            screen.blit(WBishop, (80*col, 80*row))
        elif piece == "5":
            screen.blit(BBishop, (80*col, 80*row))
        elif piece == "6" or piece == "8":
            screen.blit(WRook, (80*col, 80*row))
        elif piece == "7" or piece == "9":
            screen.blit(BRook, (80*col, 80*row))
        elif piece == "A":
            screen.blit(WQueen, (80*col, 80*row))
        elif piece == "B":
            screen.blit(BQueen, (80*col, 80*row))
        elif piece == "C" or piece == "H":
            screen.blit(WKing, (80*col, 80*row))
        elif piece == "D" or piece == "I":
            screen.blit(BKing, (80*col, 80*row))
        pieceCounter += 1

def drawEval(currentEval, screen):
    font = pygame.font.Font("freesansbold.ttf", 60)

    text = font.render(str(currentEval), True, (0, 0, 0))
    rect = text.get_rect()
    rect.center = (820, 213)
    screen.blit(text, rect)



def convertFenToElliot(fenStr):
    conversions = {
        "P":"0",
        "p":"1",
        "N":"2",
        "n":"3",
        "B":"4",
        "b":"5",
        "R":"6",
        "r":"7",
        "Q":"A",
        "q":"B",
        "K":"C",
        "k":"D"
    }

    elliotStr = ""

    for letter in fenStr:
        if letter in "12345678":
            for i in range(int(letter)):
                elliotStr += "G"
        elif letter == " ":
            break
        elif letter != "/":
            elliotStr += conversions[letter]

    return elliotStr

#####################
print(stockfish.get_fen_position())
currentElliot = convertFenToElliot(stockfish.get_fen_position())#"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

currentMove = len(uci)-1
currentEval = stockfish.get_evaluation()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_s:
                currentMove = 0
                stockfish.set_position([])
                currentEval = stockfish.get_evaluation()
                currentElliot = convertFenToElliot(stockfish.get_fen_position())

            if event.key == pygame.K_LEFT and currentMove > 0:
                currentMove -= 1

                newMoves = []
                for i in range(currentMove):
                    newMoves.append(uci[i])

                stockfish.set_position(newMoves)
                currentEval = stockfish.get_evaluation()
                currentElliot = convertFenToElliot(stockfish.get_fen_position())

            if event.key == pygame.K_RIGHT and currentMove < len(uci):
                currentMove += 1

                newMoves = []
                for i in range(currentMove):
                    newMoves.append(uci[i])

                stockfish.set_position(newMoves)
                currentEval = stockfish.get_evaluation()
                currentElliot = convertFenToElliot(stockfish.get_fen_position())



    drawBackground()
    drawEval((currentEval['value']/100), screen)
    drawPieces(currentElliot)
    pygame.display.update()
