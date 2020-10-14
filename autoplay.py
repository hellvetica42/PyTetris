from utils import *
from tetromino import *
B_WIDTH, B_HEIGHT = 10, 20

class autoplay:


    def __init__(self, coefs):
        self.C_HOLES = coefs[0]
        self.C_HEIGHT = coefs[1] 
        self.C_POINTS = coefs[2]
        self.C_PILLAR = coefs[3]
        self.C_EMPTY = coefs[4]

        self.SCORE = 0

        self.BLOCKS = [[0 for x in range(B_WIDTH)] for y in range(B_HEIGHT)]
        self.shape = tetromino()
        pass

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

        if board[3] != v_zeros:
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
        costs = [calculateBoardCost(p) for p in pred]
        minVal = min(costs)
        for p, c in zip(pred, costs):
            if c == minVal:
                # print("COST: ", c)
                self.BLOCKS = p
                self.shape = tetromino()
                self.endTurn()
                break

    def endTurn(self):
        points = self.evaluateBoard(self.BLOCKS)
        if points > 0:
            self.SCORE += points
            # print("SCORE: ", self.SCORE)
        elif points == -1:
            # print("GAME OVER")
            # print("SCORE: ", self.SCORE)
            pass

    def play(self):
        while self.evaluateBoard(self.BLOCKS) != -1:
            self.autoDrop()
        
        return self.SCORE





