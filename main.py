from chessdotcom import get_player_game_archives
import pprint
import requests
from stockfish import Stockfish
import chess
import pygame
pygame.init()

stockfish = Stockfish(r'C:\Users\ellio\Downloads\stockfish-11-win\stockfish-11-win\Windows\stockfish_20011801_x64.exe')
printer = pprint.PrettyPrinter()

stockfish._set_option("Slow Mover", 30, True)

def get_most_recent_game(username):
    data = get_player_game_archives(username).json
    url = data['archives'][-1]
    games = requests.get(url).json()
    game = games['games'][-1]
    return game['pgn']

username = input("Whose account? ")

game = get_most_recent_game(username)
#printer.pprint(game)
colorStart = game.index(username)
colorLetter = game[colorStart - 3]

if colorLetter == "k":
    print(username, "was Black")
else:
    print(username, "was White")

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


def getMissingPieces(fenStr):
    whitePieces = "RRNNBBKQPPPPPPPP"
    blackPieces = "rrnnbbkqpppppppp"

    scores = {
        "R": 5,
        "r": -5,
        "N": 3,
        "n": -3,
        "B": 3,
        "b": -3,
        "Q": 9,
        "q": -9,
        "K": 0,
        "k": 0,
        "P": 1,
        "p": -1
    }
    score = 0
    for piece in fenStr:
        if piece in whitePieces:
            newWhitePieces = ""
            taken = False
            for p in whitePieces:
                if p != piece or taken:
                    newWhitePieces += p
                else:
                    taken = True
            whitePieces = newWhitePieces
            score += scores[piece]
        if piece in blackPieces:
            newBlackPieces = ""
            taken = False
            for p in blackPieces:
                if p != piece or taken:
                    newBlackPieces += p
                else:
                    taken = True
            blackPieces = newBlackPieces
            score += scores[piece]
        if piece == " ":
            break

    return [score, whitePieces, blackPieces]


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

# and the mini ones
mBBishop = pygame.transform.scale(BBishop, (40, 40))
mBKing = pygame.transform.scale(BKing, (40, 40))
mBKnight = pygame.transform.scale(BKnight, (40, 40))
mBPawn = pygame.transform.scale(BPawn, (40, 40))
mBQueen = pygame.transform.scale(BQueen, (40, 40))
mBRook = pygame.transform.scale(BRook, (40, 40))

mWBishop = pygame.transform.scale(WBishop, (40, 40))
mWKing = pygame.transform.scale(WKing, (40, 40))
mWKnight = pygame.transform.scale(WKnight, (40, 40))
mWPawn = pygame.transform.scale(WPawn, (40, 40))
mWQueen = pygame.transform.scale(WQueen, (40, 40))
mWRook = pygame.transform.scale(WRook, (40, 40))


def drawMinis(screen, score):
    imgs = {
        "R":mWRook,
        "r":mBRook,
        "N":mWKnight,
        "n":mBKnight,
        "B":mWBishop,
        "b":mBBishop,
        "Q":mWQueen,
        "q":mBQueen,
        "P":mWPawn,
        "p":mBPawn
    }

    whiteCoords = [660, 20]

    for piece in score[1]:
        screen.blit(imgs[piece], (whiteCoords[0], whiteCoords[1]))
        whiteCoords[0] += 40
        if whiteCoords[0] > 960:
            whiteCoords[0] = 660
            whiteCoords[1] += 50

    blackCoords = [660, 500]
    for piece in score[2]:
        screen.blit(imgs[piece], (blackCoords[0], blackCoords[1]))
        blackCoords[0] += 40
        if blackCoords[0] > 960:
            blackCoords[0] = 660
            blackCoords[1] += 50

    font = pygame.font.Font("freesansbold.ttf", 20)

    if score[0] > 0:
        text = "+" + str(score[0])
        text = font.render(text, True, (100, 100, 100))
        rect = text.get_rect()
        rect.center = (blackCoords[0]+20, blackCoords[1]+20)
        screen.blit(text, rect)

    elif score[0] < 0:
        text = "+" + str(-score[0])
        text = font.render(text, True, (100, 100, 100))
        rect = text.get_rect()
        rect.center = (whiteCoords[0]+20, whiteCoords[1]+20)
        screen.blit(text, rect)


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

def drawSquareNames(screen):
    font = pygame.font.Font("freesansbold.ttf", 10)

    for i in range(8, 0, -1):
        if i % 2 == 0:
            text = font.render(str(i), True, (76,116,156))
        else:
            text = font.render(str(i), True, (236,236,212))
        rect = text.get_rect()
        rect.center = (5, 80*(8-i) + 5)
        screen.blit(text, rect)
    letters = "abcdefgh"
    for i in range(8):
        if i % 2 == 1:
            text = font.render(letters[i], True, (76, 116, 156))
        else:
            text = font.render(letters[i], True, (236, 236, 212))
        rect = text.get_rect()
        rect.center = (80*(i) + 75, 635)
        screen.blit(text, rect)

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
    if currentEval['type'] == 'mate':
        currentEval = "GG"
    else:
        currentEval = str(currentEval["value"]/100)

    font = pygame.font.Font("freesansbold.ttf", 60)

    text = font.render(str(currentEval), True, (0, 0, 0))
    rect = text.get_rect()
    rect.center = (820, 213)
    screen.blit(text, rect)

def drawBestMove(currentBestMove, screen):
    font = pygame.font.Font("freesansbold.ttf", 60)

    text = font.render(str(currentBestMove), True, (0, 0, 0))
    rect = text.get_rect()
    rect.center = (820, 426)
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
#print(stockfish.get_fen_position())
currentElliot = convertFenToElliot(stockfish.get_fen_position())#"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

def getMoveHighlight(previousMove, goodMove, computerMove, bestMove):
    previousMove = str(previousMove)
    #print(previousMove)
    if bestMove:
        symbol1 = "e"
        symbol2 = "E"
    elif computerMove:
        symbol1 = "c"
        symbol2 = "C"
    elif goodMove:
        symbol1 = "y"
        symbol2 = "Y"
    else:
        symbol1 = "b"
        symbol2 = "B"

    letters = "abcdefgh"
    col1 = letters.index(previousMove[0])
    col2 = letters.index(previousMove[2])
    row1 = 8-(int(previousMove[1]))
    row2 = 8-(int(previousMove[3]))

    #print(row1, row2, col1, col2)

    retStr = ""
    found = False

    for i in range(64):
        if i != 8*row1 + col1 and i != 8 * row2 + col2:
            retStr += "G"
        elif not found:
            retStr += symbol1
            found = True
        else:
            retStr += symbol2
    #print(retStr)
    return retStr

def judgeMove(moves, currentMove):
    moveList = []
    for i in range(currentMove-1):
        moveList.append(moves[i])
    stockfish.set_position(moveList)

    bestMoves = stockfish.get_top_moves()
    approved = []
    for move in bestMoves:
        approved.append(move['Move'])
    return str(moves[currentMove - 1]) in approved

startMoves = []
for i in range(len(uci)-1):
    startMoves.append(uci[i])
stockfish.set_position(startMoves)
prevBestMove = stockfish.get_best_move()
stockfish.make_moves_from_current_position([uci[len(uci)-1]])

currentMove = len(uci)
currentEval = stockfish.get_evaluation()
prevEval = currentEval
currentBestMove = stockfish.get_best_move()
goodMove = judgeMove(uci, currentMove)
computerMove = False
moveHighlight = getMoveHighlight(str(uci[currentMove-1]), goodMove, computerMove, False)
prevBestHighlight = "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
prevBestHighlight = getMoveHighlight(prevBestMove, False, False, True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_s:
                moveHighlight = "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
                prevBestHighlight = "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
                currentMove = 0
                stockfish.set_position([])
                prevEval = 0.67
                currentEval = stockfish.get_evaluation()
                currentBestMove = stockfish.get_best_move()
                prevBestHighlight = getMoveHighlight(currentBestMove, False, False, True)
                currentElliot = convertFenToElliot(stockfish.get_fen_position())

            if event.key == pygame.K_LEFT and currentMove > 0:
                currentMove -= 1
                newMoves = []
                for i in range(currentMove - 1):
                    newMoves.append(uci[i])

                stockfish.set_position(newMoves)
                currentBestMove = stockfish.get_best_move()
                try:
                    pastMove = uci[currentMove-1]
                    stockfish.make_moves_from_current_position(computerMove)
                    #print("computer moved")
                    bestEval = stockfish.get_evaluation()
                    stockfish.set_position(newMoves)
                    #print("reset")
                    #print(stockfish.get_board_visual())
                    #print(uci[currentMove-1])
                    stockfish.make_moves_from_current_position([str(uci[currentMove-1])])
                    #print("player move")
                    evalDifference = bestEval['value'] - stockfish.get_evaluation()['value']
                    if abs(evalDifference) > 100:
                        goodMove = False
                    else:
                        goodMove = True
                    #goodMove = judgeMove(uci, currentMove)
                    stockfish.set_position(newMoves)
                    #print("reset")
                    moveHighlight = getMoveHighlight(pastMove, goodMove, computerMove, False)
                except:
                    moveHighlight = "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"

                prevBestHighlight = getMoveHighlight(currentBestMove, False, False, True)

                try:
                    stockfish.set_position(newMoves)
                    stockfish.make_moves_from_current_position([uci[currentMove - 1]])
                    newMoves.append(uci[currentMove-1])
                except:
                    stockfish.set_position([])

                currentEval = stockfish.get_evaluation()
                currentBestMove = stockfish.get_best_move()
                currentElliot = convertFenToElliot(stockfish.get_fen_position())

            if event.key == pygame.K_RIGHT and currentMove < len(uci):
                currentMove += 1

                newMoves = []
                for i in range(currentMove):
                    newMoves.append(uci[i])

                stockfish.set_position(newMoves)
                prevEval = currentEval
                currentEval = stockfish.get_evaluation()


                try:
                    pastMove = newMoves[-1]
                    deltaEval = currentEval['value'] - prevEval['value']
                    if abs(deltaEval) >= 100:
                        goodMove = False
                    elif str(pastMove) == computerMove:
                        goodMove = True
                    else:
                        goodMove = True
                    moveHighlight = getMoveHighlight(pastMove, goodMove, computerMove, False)
                except:
                    moveHighlight = "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
                    prevBestHighlight = "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
                stockfish.set_position(newMoves)


                prevBestHighlight = getMoveHighlight(currentBestMove, False, False, True)

                currentBestMove = stockfish.get_best_move()
                currentElliot = convertFenToElliot(stockfish.get_fen_position())

            if event.key == pygame.K_p:
                prevBestHighlight = "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
                try:
                    computerMove = True
                    newBest = stockfish.get_best_move()
                    moveHighlight = getMoveHighlight(newBest, True, computerMove, False)
                    stockfish.make_moves_from_current_position([newBest])
                    currentEval = stockfish.get_evaluation()
                    currentBestMove = stockfish.get_best_move()
                    currentElliot = convertFenToElliot(stockfish.get_fen_position())
                except:
                    pass

            if event.key == pygame.K_r:
                computerMove = False
                newMoves = []
                for i in range(currentMove-1):
                    newMoves.append(uci[i])
                stockfish.set_position(newMoves)
                currentBestMove = stockfish.get_best_move()
                newMoves.append(uci[currentMove-1])
                try:
                    pastMove = newMoves[-1]
                    goodMove = judgeMove(uci, currentMove)
                    moveHighlight = getMoveHighlight(pastMove, goodMove, computerMove, False)
                except:
                    moveHighlight = "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"

                prevBestHighlight = getMoveHighlight(currentBestMove, False, False, True)

                try:
                    stockfish.make_moves_from_current_position([uci[currentMove-1]])
                except:
                    stockfish.set_position([])
                currentEval = stockfish.get_evaluation()
                currentBestMove = stockfish.get_best_move()
                currentElliot = convertFenToElliot(stockfish.get_fen_position())



    #print(prevBestHighlight)
    drawBackground()
    drawEval((currentEval), screen)
    drawBestMove(currentBestMove, screen)
    if moveHighlight != "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG":
        if computerMove:
            pygame.draw.rect(screen, (100, 100, 200), pygame.Rect(moveHighlight.index("c") % 8 * 80, moveHighlight.index("c") // 8 * 80, 80, 80))
            pygame.draw.rect(screen, (100, 100, 200),
                             pygame.Rect(moveHighlight.index("C") % 8 * 80, moveHighlight.index("C") // 8 * 80, 80, 80))
        elif goodMove:
            pygame.draw.rect(screen, (100, 200, 100),
                     pygame.Rect(moveHighlight.index("y") % 8 * 80, moveHighlight.index("y") // 8 * 80, 80, 80))
            pygame.draw.rect(screen, (100, 200, 100),
                             pygame.Rect(moveHighlight.index("Y") % 8 * 80, moveHighlight.index("Y") // 8 * 80, 80, 80))
        else:
            pygame.draw.rect(screen, (200, 100, 100),
                     pygame.Rect(moveHighlight.index("b") % 8 * 80, moveHighlight.index("b") // 8 * 80, 80, 80))
            pygame.draw.rect(screen, (200, 100, 100),
                             pygame.Rect(moveHighlight.index("B") % 8 * 80, moveHighlight.index("B") // 8 * 80, 80, 80))
    if prevBestHighlight != "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG":
        pygame.draw.rect(screen, (100, 200, 200),
                         pygame.Rect(prevBestHighlight.index("e") % 8 * 80, prevBestHighlight.index("e") // 8 * 80, 80, 80))
        pygame.draw.rect(screen, (100, 200, 200),
                         pygame.Rect(prevBestHighlight.index("E") % 8 * 80, prevBestHighlight.index("E") // 8 * 80, 80, 80))

    missingPieces = getMissingPieces(stockfish.get_fen_position())
    drawMinis(screen, missingPieces)

    drawSquareNames(screen)
    drawPieces(currentElliot)
    pygame.display.update()
