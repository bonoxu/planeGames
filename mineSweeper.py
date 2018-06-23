import numpy as np
import random
import time
class Square():
    def __init__(self, **keywords):
        self.m_masked = keywords.get("masked", True)
        self.m_isMine = keywords.get("isMine", False)
        self.m_nearbyMine = keywords.get("nearbyMine", 0)
        self.m_isMarked = keywords.get("isMarked", False)

def initialise(height, width):
    board = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(Square())
        board.append(row)
    return board

def isNeighbour(i, j, newI, newJ):
    if i == newI and j == newJ:
        return False
    if abs(i - newI) <= 1 and abs(j - newJ) <= 1:
        return True

def isAdjacent(i, j, newI, newJ):
    if i == newI and j == newJ:
        return False
    if (abs(i - newI) == 1 and j == newJ) or (abs(j - newJ) == 1 and i == newI):
        return True

def isAdjacentArr(i, j, myArray):
    for newI, newJ in myArray:
        if isNeighbour(i, j, newI, newJ):
            return True
    return False

def isAdjacentZeroArr(i, j, myArray, board):
    for newI, newJ in myArray:
        if isNeighbour(i, j, newI, newJ) and board[newI][newJ].m_nearbyMine == 0:
            return True
    return False

def expandClickImpl(board, myList):
    addFlag = False
    for i in range(len(board)):
        for j in range(len(board[i])):
            if inBoard(board, i, j) and not board[i][j].m_isMine and isAdjacentZeroArr(i, j, myList, board):
                if (i,j) not in myList:
                    myList.append((i, j))
                    addFlag = True
    return myList, addFlag

def expandClick(board, currentI, currentJ):
    myList = [(currentI, currentJ)]
    lostFlag = False
    if board[currentI][currentJ].m_nearbyMine == 0 and board[currentI][currentJ].m_masked:
        while True:
            myList, addFlag = expandClickImpl(board, myList)
            if not addFlag:
                break

    elif not board[currentI][currentJ].m_masked:
        markedMineCount = 0
        markedUnmineCount = 0
        for i in range(currentI-1, currentI+2):
            for j in range(currentJ-1, currentJ+2):
                if i == currentI and j == currentJ:
                    continue
                if inBoard(board, i, j) and board[i][j].m_isMine and board[i][j].m_isMarked:
                    markedMineCount += 1
                elif inBoard(board, i, j) and not board[i][j].m_isMine and board[i][j].m_isMarked:
                    markedUnmineCount += 1

        if markedUnmineCount == 0 and markedMineCount == board[currentI][currentJ].m_nearbyMine:
            for i in range(currentI-1, currentI+2):
                for j in range(currentJ-1, currentJ+2):
                    if i == currentI and j == currentJ:
                        continue
                    if inBoard(board, i, j) and not board[i][j].m_isMine:
                        myList.append((i, j))
        else:
            lostFlag = True
        while True:
            myList, addFlag = expandClickImpl(board, myList)
            if not addFlag:
                break

    for i, j in myList:
        board[i][j].m_masked = False
        board[i][j].m_isMarked = False
    return board, lostFlag

def checkWin(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].m_isMine:
                continue
            if board[i][j].m_masked:
                #print i,j, board[i][j].m_isMine, board[i][j].m_masked, board[i][j].m_isMarked
                return False
    return True

def getIntStr(number):
    if number < 10:
        return str(number) + " "
    else:
        return str(number)

from Tkinter import *

class MyFirstGUI:
    def __init__(self, **keywords):
        self.master = keywords.get("master", None)
        self.master.title("A simple GUI")
        self.board = keywords.get("board", None)
        self.label = Label(self.master, text="")
        #self.label.pack()
        self.label.grid(columnspan=2, sticky=W)
        self.buttons = []
        for i in range(len(self.board)):
            buttons = []
            for j in range(len(self.board[i])):
                myButton = Button(self.master, text="  ", command = lambda iTemp = i, jTemp = j: self.leftClick(iTemp,jTemp))
                myButton.grid(row = i, column = j)
                buttons.append(myButton)
            self.buttons.append(buttons)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.buttons[i][j].bind('<Button-2>', lambda iTemp = i, jTemp = j: self.rightClick(event, iTemp,jTemp))

                #self.buttons[i][j].configure(command=self.greet(i,j))
        #self.greet_button = Button(self.master, text="Greet", command=self.greet)
        #self.greet_button.grid(row = 1)

        #self.close_button = Button(self.master, text="Close", command=self.master.quit)
        #self.close_button.grid(row = 1, column = 1)

    def leftClick(self, i, j):
        #print i,j
        if self.board[i][j].m_masked:
            self.board[i][j].m_masked = False

            self.buttons[i][j]["text"] = str(self.board[i][j].m_nearbyMine)
        #self.buttons[i][j]["text"] = "a"

    def rightClick(self, event):
        print i,j
        self.buttons[i][j]["text"] = "b"

def visualiseGUI(board):
    root = Tk()
    my_gui = MyFirstGUI(master = root, board = board)
    root.mainloop()

def visualise(board):

    visualiseGUI(board)

    rowStr = "mine left " + str(totalMine(board) - markedMine(board)) + "/" + str(totalMine(board)) + "\n"
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
            if board[i][j].m_masked:
                rowStr += "." + virtialDivider
            elif board[i][j].m_isMarked:
                rowStr += "^" + virtialDivider
            else:
                if board[i][j].m_isMine:
                    rowStr += "*" + virtialDivider
                else:
                    rowStr += str(board[i][j].m_nearbyMine) + virtialDivider
        rowStr += "\n"
    print rowStr

def randomMine(board, prob):
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j].m_isMine = True if random.random() < prob else False
    return board

def inBoard(board, currentHeight, currentWidth):
    if len(board) == 0:
        return False
    return currentHeight >=0 and currentHeight < len(board) and currentWidth >= 0 and currentWidth < len(board[0])

def countMine(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            counter = 0
            for iMove in range(i - 1, i + 2):
                for jMove in range(j - 1, j + 2):
                    if iMove == i and jMove == j:
                        continue
                    if inBoard(board, iMove, jMove) and board[iMove][jMove].m_isMine:
                        counter += 1
            board[i][j].m_nearbyMine = counter
    return board

def totalMine(board):
    counter = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].m_isMine:
                counter += 1
    return counter

def markedMine(board):
    counter = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].m_isMarked:
                counter += 1
    return counter

def lostEnding(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j].m_masked = False
            board[i][j].m_isMarked = False
    visualise(board)
def play(board):

    while True:
        while True:
            try:
                myInput = input("Input format: Row, Column, Mark Mine(optional) ")
                # check my Input
                if len(myInput) != 2 and len(myInput) != 3:
                    print "Invalid input; Try again"
                elif myInput[0] < 0 or myInput[0] >= len(board) or myInput[1] < 0 or  myInput[1] >= len(board[0]):
                    print "Invalid input; Outside the board Try again"
                else:
                    height = int(myInput[0])
                    width = int(myInput[1])
                    marked = False if len(myInput) == 2 else True
                    break
            except:
                print "Invalid input; Try again"


        if marked:
            if board[height][width].m_isMarked:
                board[height][width].m_isMarked = False
                board[height][width].m_masked = True
            else:
                if not board[height][width].m_masked:
                    print "Can not mark non-mine", (height, width)
                else:
                    board[height][width].m_isMarked = True
                    board[height][width].m_masked = False
            #board[height][width].m_isMarked = not board[height][width].m_isMarked
            visualise(board)
        else:
            if board[height][width].m_isMine:
                print "Clicked on Mine;", (height, width), " Game lost! Sad"
                lostEnding(board)
                break
            else:
                board, lostFlag = expandClick(board, height, width)
                if not lostFlag:
                #board[height][width].m_masked = False
                    visualise(board)
                else:
                    print "Wrong expanding;", (height, width), " Game lost! Sad"
                    lostEnding(board)
                    break
        if checkWin(board):
            print "Congratulation!"
            visualise(board)
            break
if __name__ == '__main__':
    try:
        print "default board size 12x12, mine porbability 20%"
        boardHeight, boardWidth, prob = input("Board height, board width, probability; i.e. 12, 12, 0.2 ")

        board = initialise(boardHeight,boardHeight)
        board = randomMine(board, prob)
    except:
        board = initialise(12,12)
        board = randomMine(board, 0.2)
    board = countMine(board)
    visualise(board)
    startTime = time.time()
    play(board)
    endTime = time.time()
    print "total mine ", totalMine(board), "startTime ", startTime, " endTime ", endTime, " cost ", endTime - startTime
