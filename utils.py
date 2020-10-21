import copy
C_HOLES = 3.5
C_HEIGHT = 3
C_PILLAR = 2
C_OVERHANG = 2.3
C_BUMPINESS = 2
C_BLOCKS = 3.5
C_LASTCOL = 2
C_POINTS = 5

C_LINES = 1
C_EMPTY = 3


def calculateBoardCost(board):
    cost = 0
    cost += C_HOLES * getNumHoles(board)
    cost += C_HEIGHT * getBoardHeight(board)
    cost += C_PILLAR * getEmptyPillarBlocks(board)
    cost += C_OVERHANG * getOverhangs(board)
    cost += C_BUMPINESS * getBumpiness(board)
    cost += C_BLOCKS * getBlocksOverHoles(board)
    cost += C_LASTCOL * getNumBlocksInLastCol(board)
    # cost += C_LINES * getEmptyLineBlocks(board)
    # cost += C_EMPTY * getEmptyBlocksBelowTallest(board)
    cost -= C_POINTS * getBoardPoints(board)

    return cost

def getNumHoles(board):
    holes = 0

    def floodFill(b, x, y, count):
        #if out of range
        if y < 0 or y >= len(b) or x < 0 or x >= len(b[y]):
            return 0

        # if already visited
        if b[y][x] == -1:
            return 0
        # if not empty
        elif b[y][x] != 0:
            return 0
        else:
            b[y][x] = -1
            count += 1
        
            floodFill(b, x, y-1, count)
            floodFill(b, x, y+1, count)
            floodFill(b, x-1, y, count)
            floodFill(b, x+1, y, count)

        return count

    tmpBoard = copy.deepcopy(board)

    for y in range(len(board)):
        for x in range(len(board[y])):
            if tmpBoard[y][x] == 0:
                holeSize = floodFill(tmpBoard, x, y, 0) 
                if holeSize < 20 and holeSize > 0:
                    holes += holeSize


    return holes

def getBumpiness(board):

    def getColHeight(x):
        for y in range(len(board)):
            if board[y][x] == 1:
                return len(board) - y
        return 0

    colHeights = [getColHeight(x) for x in range(len(board[0]))]

    bumpiness = sum([abs(colHeights[i] - colHeights[i+1]) for i in range(len(colHeights)-1)])

    return bumpiness


    




def getBoardHeight(board):
    height = 0
    y = 0
    v_zeros = [0 for i in range(len(board[0]))]
    while board[y] == v_zeros:
        y += 1

    return len(board) - y 

def getBoardPoints(board):

    v_ones = [1 for i in range(len(board[0]))]
    v_zeros = [0 for i in range(len(board[0]))]
    to_remove = 0

    if board[0] != v_zeros:
        return -1

    for y in range(len(board)):
        if board[y] == v_ones:
            to_remove += 1


    if to_remove >= 4:
        to_remove *= 2
    
    return to_remove

def getEmptyPillarBlocks(board):
    #blocks that are empty on opposite sides
    count = 0

    tmpB = copy.deepcopy(board)

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 0:
                #if its a pillar block
                if y-1 < 0 or board[y-1][x] == 0 or board[y-1][x] == -1:
                    if y+1 >= len(board) or board[y+1][x] == 0 or board[y-1][x] == -1:
                        if x-1 < 0 or board[y][x-1] == 1:
                            if x+1 >= len(board[y]) or board[y][x+1] == 1:
                                tmpB[y][x] = -1

    for y in range(len(tmpB)):
        for x in range(len(tmpB[y])):
            if tmpB[y][x] == -1:
                tmpY = y 
                c = 1
                while tmpY < len(tmpB) and tmpB[tmpY][x] == -1:
                    tmpB[tmpY][x] = 2
                    tmpY += 1
                    c += 1

                if c >= 3:
                    count += c
    return count 

def getOverhangs(board):
    count = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 0:
                if y-1 < 0 or board[y-1][x] == 1:
                    # if y+1 >= len(board) or board[y+1][x] == 1:
                    #     #UP and DOWN are blocks

                    #     #if leftside empty
                    #     if x-1 >= 0 and board[y][x-1] == 0:
                    #         if x+1 >= len(board[y]) or board[y][x+1] == 1:
                    #             count += 1
                    #     #if rightside empty
                    #     elif x+1 < len(board[y]) and board[y][x+1] == 0:
                    #         if x-1 < 0 or board[y][x-1] == 1:
                    #             count += 1
                    # #if down is empty 
                    # elif y+1 < len(board) and board[y+1][x] == 0:
                    #     count += 1
                    count += 1
                    

    return count

def getNumBlocksInLastCol(board):
    count = 0
    for y in board:
        if y[-1] == 1:
            count += 1

    return count

def getBlocksOverHoles(board):
    count = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 0:

                if y-1 < 0 or board[y-1][x] == 1:
                    if y+1 >= len(board) or board[y+1][x] == 1:
                        if x-1 < 0 or board[y][x-1] == 1:
                            if x+1 >= len(board[y]) or board[y][x+1] == 1:
                                c = 0
                                y -= 1
                                while board[y][x] == 1: 
                                    y -= 1
                                    c += 1
                                count += c

    return count
                                


