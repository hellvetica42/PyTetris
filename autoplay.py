from utils import *
from tetromino import *
import concurrent.futures
B_WIDTH, B_HEIGHT = 10, 20

class autoplay:


    def __init__(self, coefs):
        self.coefs = coefs
        self.C_HOLES = coefs[0]
        self.C_HEIGHT = coefs[1] 
        self.C_PILLAR = coefs[2]
        self.C_OVERHANG = coefs[3]
        self.C_BUMPINESS = coefs[4]
        self.C_BLOCKS = coefs[5]
        self.C_LASTCOL = coefs[6]
        self.C_POINTS = coefs[7]

        self.SCORE = 0

        self.BLOCKS = [[0 for x in range(B_WIDTH)] for y in range(B_HEIGHT)]
        self.shape = tetromino()
        self.heldShape = tetromino()
        pass

    def reset(self):
        self.SCORE = 0

        self.BLOCKS = [[0 for x in range(B_WIDTH)] for y in range(B_HEIGHT)]
        self.shape = tetromino()
        self.heldShape = tetromino()

    def calculateBoardCost(self, board):
        cost = 0

        cost += self.C_HOLES * getNumHoles(board)
        cost += self.C_HEIGHT * getBoardHeight(board)
        cost += self.C_PILLAR * getEmptyPillarBlocks(board)
        cost += self.C_OVERHANG * getOverhangs(board)
        cost += self.C_BUMPINESS * getBumpiness(board)
        cost += self.C_BLOCKS * getNumBlocksInLastCol(board)
        cost += self.C_LASTCOL * getNumBlocksInLastCol(board)
        # cost += self.C_EMPTY * getEmptyBlocksBelowTallest(board)
        cost -= self.C_POINTS * getBoardPoints(board)

        return cost

    def getCoefs(self):
        return self.coefs

    def setCoefs(self, coefs):
        self.coefs = coefs
        self.C_HOLES = coefs[0]
        self.C_HEIGHT = coefs[1] 
        self.C_PILLAR = coefs[2]
        self.C_OVERHANG = coefs[3]
        self.C_BUMPINESS = coefs[4]
        self.C_BLOCKS = coefs[5]
        self.C_LASTCOL = coefs[6]
        self.C_POINTS = coefs[7]



    def getBoard(self):
        return self.BLOCKS

    #if shape can be moved to x, y on tris board. Returns True/False
    def canBeMoved(self, board, sh, x, y):
        for sy in range(len(sh)):
            for sx in range(len(sh[sy])):
                if sh[sy][sx] == 1 and (x + sx < 0 or x + sx >= B_WIDTH):
                    return False
                if sh[sy][sx] == 1 and (y + sy < 0 or y + sy >= B_HEIGHT):
                    return False
                if sh[sy][sx] == 1 and board[y + sy][x + sx] == 1:
                    return False
        
        return True

    #Set the shape into the given board
    def bindShape(self, board, sh):
        for sy in range(len(sh.getShape())):
            for sx in range(len(sh.getShape()[sy])):
                    if sh.getShape()[sy][sx] == 1:
                        cy = sh.getPosY() + sy
                        cx = sh.getPosX() + sx
                        board[cy][cx] = 1

    def evaluateBoard(self, board):
        v_ones = [1 for i in range(B_WIDTH)]
        v_zeros = [0 for i in range(B_WIDTH)]
        to_remove = []

        if board[1] != v_zeros:
            return -1

        for y in range(len(board)):
            if board[y] == v_ones:
                to_remove.append(y)
        
        for y in to_remove:
            for i in range(y, 0, -1):
                board[i] = board[i-1].copy()

        return len(to_remove)

    def getAllFuturePositions(self, board, sh):
        result = []

        for i in range(sh.getNumRotations()):

            sh.setRotation(i)

            x = 0
            y = 0
            while self.canBeMoved(board, sh.getShape(), x, 0):
                x -= 1

            x += 1

            while self.canBeMoved(board, sh.getShape(), x, 0):
                while self.canBeMoved(board, sh.getShape(), x, y):
                    y += 1
                
                y -= 1

                sh.setPosX(x)
                sh.setPosY(y)

                tmp = copy.deepcopy(board) 

                self.bindShape(tmp, sh)

                result.append(tmp)

                x += 1
                y = 0

                sh.setPosX(0)
                sh.setPosY(0)

        return result

    def autoDrop(self):
        
        pred = self.getAllFuturePositions(self.BLOCKS, self.shape)
        predHeld = self.getAllFuturePositions(self.BLOCKS, self.heldShape)

        costs = [self.calculateBoardCost(p) for p in pred]
        costsHeld = [self.calculateBoardCost(p) for p in predHeld]

        minVal = min(costs)
        minValHeld = min(costsHeld)

        if minValHeld < minVal:
            tmp = self.shape
            self.shape = self.heldShape
            self.heldShape = tmp
            pred = predHeld
            costs = costsHeld
            minVal = minValHeld

        minIndex = costs.index(minVal)
        self.BLOCKS = pred[minIndex]
        self.shape = tetromino()
        self.endTurn()

    def endTurn(self):
        points = self.evaluateBoard(self.BLOCKS)
        if points > 0:
            self.SCORE += points
            # print("SCORE: ", self.SCORE)
        elif points == -1:
            # print("GAME OVER")
            # print("SCORE: ", self.SCORE)
            pass

    def getScore(self):
        return self.SCORE
        
    def play(self):
        while self.evaluateBoard(self.BLOCKS) != -1:
            self.autoDrop()
        
        return self.SCORE





