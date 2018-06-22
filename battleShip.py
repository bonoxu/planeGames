CARRIER = 1
BATTLESHIP = 5
DESTROYER = 2
SUBMERAINE = 3
FRIGATE = 4
DICT = {CARRIER : "C", BATTLESHIP : "B", DESTROYER: "D", SUBMERAINE: "S", FRIGATE: "F"}
HITDICT = {CARRIER : "c", BATTLESHIP : "b", DESTROYER: "d", SUBMERAINE: "s", FRIGATE: "f"}
FULLDICT = {CARRIER : ("Carrier", 4), BATTLESHIP : ("Battleship", 3), DESTROYER: ("Destroyer", 3) \
    , SUBMERAINE: ("Submariane", 3), FRIGATE: ("Frigate", 2)}

DIRECTION = ["U","D","L","R"]
def getNewCorridate(i,j, direction, step):
    if direction == 1:
        return i-step, j
    elif direction == 2:
        return i+step, j
    elif direction == 3:
        return i, j-step
    elif direction == 4:
        return i, j+step
    else:
        return -1,-1
class Board():
    def __init__(self, **keywords):
        self.m_board = keywords.get("board", None)
        self.m_playerName = keywords.get("playerName", "Easy")
    def initialise(self,height, width):
        self.m_board = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Square())
            self.m_board.append(row)
    def inBoard(self, currentHeight, currentWidth):
        if len(self.m_board) == 0:
            return False
        return currentHeight >=0 and currentHeight < len(self.m_board) and currentWidth >= 0 and currentWidth < len(self.m_board[0])

    def setup(self):
        #Carrier 1 x 4; 3 1x3; 1x2
        #for i in range(30):
        #    print "\n"

        #print("New player")
        visualise(self, noMaskFlag = True)

        for key, item in FULLDICT.iteritems():
            nameStr, length = item
            while True:
                try:
                    myInput = input(nameStr + " input first first coordinate and direction(U=1,D=2,L=3,R=4) i.e. 1,2,4 ")
                    # check my Input
                    #print myInput
                    height = int(myInput[0])
                    width = int(myInput[1])
                    direction = int(myInput[2])

                    coordinates = []
                    for i in range(length):
                        newHeight, newWidth = getNewCorridate(height,width, direction, i)

                        if not self.inBoard(newHeight, newWidth) or self.m_board[newHeight][newWidth].m_hasShip:
                            raise exception("")
                        else:
                            coordinates.append((newHeight, newWidth))
                    for i, j in coordinates:
                        self.m_board[i][j].m_hasShip = True
                        self.m_board[i][j].m_ship = key
                        #print i,j
                    visualise(self, noMaskFlag = True)
                    break
                except:
                    print "Invalid input; Try again"

            #print height, width, direction
def clearScreen():
    for i in range(30):
        print "\n"
class Square():
    def __init__(self, **keywords):
        self.m_masked = keywords.get("masked", True)
        self.m_isHit = keywords.get("isHit", False)
        self.m_hasShip = keywords.get("hasShip", False)
        self.m_ship = keywords.get("ship", None)

def visualise(boardObject, noMaskFlag = False):
    board = boardObject.m_board
    rowStr = "Player " + boardObject.m_playerName + "\n"
    virtialDivider = "| "
    for i in range(len(board)):
        # horizontal boarder
        if i == 0:
            rowStr += "    "
            for j in range(len(board[i])):
                rowStr += getIntStr(j) + " "
            rowStr += "\n"
            for j in range(len(board[i]) + 1):
                rowStr += "---"
            rowStr += "\n"
        for j in range(len(board[i])):
            if j == 0: # vertical boarder
                rowStr += getIntStr(i)+"| "
            if not noMaskFlag:
                if board[i][j].m_masked:
                    rowStr += "." + virtialDivider
                elif board[i][j].m_isHit and not board[i][j].m_hasShip:
                    rowStr += "*" + virtialDivider
                elif board[i][j].m_isHit and board[i][j].m_hasShip:
                    rowStr += HITDICT[board[i][j].m_ship] + virtialDivider
                elif board[i][j].m_hasShip:
                    rowStr += DICT[board[i][j].m_ship] + virtialDivider
            else:
                if not board[i][j].m_isHit and not board[i][j].m_hasShip:
                    rowStr += "." + virtialDivider
                elif board[i][j].m_isHit and not board[i][j].m_hasShip:
                    rowStr += "*" + virtialDivider
                elif board[i][j].m_isHit and board[i][j].m_hasShip:
                    rowStr += HITDICT[board[i][j].m_ship] + virtialDivider
                elif board[i][j].m_hasShip:
                    rowStr += DICT[board[i][j].m_ship] + virtialDivider

        rowStr += "\n"
    print rowStr
def lose(board):
    surviveFlag = False
    for i in range(len(board.m_board)):
        for j in range(len(board.m_board[i])):
            if board.m_board[i][j].m_hasShip and not board.m_board[i][j].m_isHit:
                surviveFlag = True
    return not surviveFlag

def play(boardL, boardR):
    myBoard = boardL
    opponentBoard = boardR
    while True:
        visualise(myBoard, noMaskFlag = True)
        visualise(opponentBoard)
        continueFlag = False
        while True:
            try:
                myInput = input("cooridnate row by column to hit")
                height = int(myInput[0])
                width = int(myInput[1])
                if opponentBoard.inBoard(height, width) and not opponentBoard.m_board[height][width].m_isHit:
                    opponentBoard.m_board[height][width].m_isHit = True
                    opponentBoard.m_board[height][width].m_masked = False
                    if opponentBoard.m_board[height][width].m_hasShip:
                        continueFlag = True
                    break
            except:
                print "Invalid input; Try again"
        if lose(opponentBoard):
            print "You won"
            visualise(myBoard, noMaskFlag = True)
            visualise(opponentBoard, noMaskFlag = True)
            break

        if not continueFlag:
            tempBoard = myBoard
            myBoard = opponentBoard
            opponentBoard = tempBoard
            print "Rotate player"
            raw_input("press any and pass on to next player")
            clearScreen()
            raw_input("press any to continue")
        else:
            print "Good hit"

        #break
def getIntStr(number):
    if number < 10:
        return str(number) + " "
    else:
        return str(number)
if __name__ == '__main__':
    board = Board(playerName = "1")
    try:
        print "default board size 8x8"
        boardHeight, boardWidth = input("Board height, board width; i.e. 8,8 ")

        board.initialise(boardHeight,boardHeight)

    except:
        board.initialise(8,8)
    import copy
    boardR = copy.deepcopy(board)
    boardR.m_playerName = "2"
    #visualise(board)
    board.setup()
    clearScreen()
    boardR.setup()
    clearScreen()
    raw_input("press any to continue. Give to other player to start the game")
    clearScreen()
    play(board, boardR)
