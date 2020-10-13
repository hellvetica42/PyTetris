import sys, pygame, random, copy
from tetromino import *
from utils import *
WIDTH, HEIGHT = 500, 1000
B_WIDTH, B_HEIGHT = 10, 20
CELL_SIZE = WIDTH/B_WIDTH

BLOCKS = [[0 for x in range(B_WIDTH)] for y in range(B_HEIGHT)]
BLOCK_COLORS = [[(0,0,0) for x in range(B_WIDTH)] for y in range(B_HEIGHT)]
shape = tetromino()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TETRIS")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))
screen.blit(background, (0,0))
pygame.display.flip()
clock = pygame.time.Clock()

SCORE = 0

#Draws shape on screen. Used only for active shape
def drawShape(x, y, shape, color, sc):
    for sy in range(len(shape)): 
        for sx in range(len(shape[sy])):
            if shape[sy][sx] == 1:
                pygame.draw.rect(sc, color, [(x+sx)*CELL_SIZE, (y+sy)*CELL_SIZE, CELL_SIZE, CELL_SIZE])
                pygame.draw.rect(sc, (0,0,0), [(x+sx)*CELL_SIZE, (y+sy)*CELL_SIZE, CELL_SIZE, CELL_SIZE], 5)

#if shape can be moved to x, y on tris board. Returns True/False
def canBeMoved(board, sh, x, y):
    for sy in range(len(sh)):
        for sx in range(len(sh[sy])):
            if sh[sy][sx] == 1 and (x + sx < 0 or x + sx >= B_WIDTH):
                return False
            if sh[sy][sx] == 1 and (y + sy < 0 or y + sy >= B_HEIGHT):
                return False
            if sh[sy][sx] == 1 and board[y + sy][x + sx] == 1:
                return False
    
    return True

#How much to offset shape in x if some pixels are off screen. Returns +-x
def getRotationOffset(sh, x, y):
    offset = 0
    for sy in range(len(sh)):
        for sx in range(len(sh[sy])):
            if sh[sy][sx] == 1 and x + sx < 0:
                offset += 1

            if sh[sy][sx] == 1 and x + sx >= B_WIDTH:
                offset -= 1

            try:
                if sh[sy][sx] == 1 and BLOCKS[y+sy][x+sx] == 1:
                    return 5 #find a better way to do this

                if y+sy >= B_HEIGHT:
                    return 5
                
            except IndexError:
                pass

    if abs(offset) == 2 and len(sh) == 3:
        if offset < 0:
            offset = -1
        elif offset > 0:
            offset = 1

    return offset

#Set the shape into the given board
def bindShape(board, boardColors, sh):
    for sy in range(len(sh.getShape())):
        for sx in range(len(sh.getShape()[sy])):
                if sh.getShape()[sy][sx] == 1:
                    board[sh.getPosY() + sy][sh.getPosX() + sx] = 1
                    boardColors[sh.getPosY() + sy][sh.getPosX() + sx] = sh.color

def evaluateBoard(board, boardColor):
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
            # if board[i] == v_zeros:
            #     break
            board[i] = board[i-1]
            boardColor[i] = boardColor[i-1]

    return len(to_remove)

def drawBoard(board, boardColor):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 1:
                pygame.draw.rect(screen, boardColor[y][x], [x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE])
                pygame.draw.rect(screen, (0,0,0), [x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE], 5)

def getAllFuturePositions(board, boardColor, sh):
    result = []
    resultColors = []

    for i in range(sh.getNumRotations()):

        sh.setRotation(i)

        x = 0
        y = 0
        while canBeMoved(board, sh.getShape(), x, 0):
            x -= 1

        x += 1

        while canBeMoved(board, sh.getShape(), x, 0):
            while canBeMoved(board, sh.getShape(), x, y):
                y += 1
            
            y -= 1

            sh.setPosX(x)
            sh.setPosY(y)

            tmp = copy.deepcopy(board) 
            tmpC = copy.deepcopy(boardColor)

            bindShape(tmp, tmpC, sh)

            result.append(tmp)
            resultColors.append(tmpC)

            x += 1
            y = 0

            sh.setPosX(0)
            sh.setPosY(0)

    return result, resultColors 

#Last event of dropping
def endTurn():
    global SCORE
    points = evaluateBoard(BLOCKS, BLOCK_COLORS)
    points = 1
    if points > 0:
        SCORE += points
        print("SCORE: ", SCORE)
    elif points == -1:
        print("GAME OVER")
        print("SCORE: ", SCORE)
        while True:
            pass

def autoDrop():
    global BLOCKS
    global BLOCK_COLORS
    global shape
    pred, predC = getAllFuturePositions(BLOCKS, BLOCK_COLORS, shape)
    costs = [calculateBoardCost(p) for p in pred]
    minVal = min(costs)
    for p, pC, c in zip(pred, predC, costs):
        # background.fill((250, 250, 250))
        # screen.blit(background, (0,0))
        # drawBoard(p, pC)
        # pygame.display.flip()
        if c == minVal:
            print("COST: ", c)
            BLOCKS = p
            BLOCK_COLORS = pC
            shape = tetromino()
            # for b in BLOCKS:
            #     print(b)
            endTurn()
            break


# pygame.time.set_timer(pygame.USEREVENT, 500)
while 1:
    clock.tick(30)
    background.fill((250, 250, 250))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                if canBeMoved(BLOCKS, shape.getShape(), shape.getPosX() - 1, shape.getPosY()):
                    shape.setPosX(shape.getPosX() - 1)

            if event.key == pygame.K_RIGHT:
                if canBeMoved(BLOCKS, shape.getShape(), shape.getPosX() + 1, shape.getPosY()):
                    shape.setPosX(shape.getPosX() + 1)

            if event.key == pygame.K_UP:
                offset = getRotationOffset(shape.getRotated(), shape.getPosX(), shape.getPosY())
                if offset != 5:
                    shape.setPosX(shape.getPosX() + offset)
                    shape.rotate()

            if event.key == pygame.K_DOWN:
                if canBeMoved(BLOCKS, shape.getShape(), shape.getPosX(), shape.getPosY() + 1):
                    shape.setPosY(shape.getPosY() + 1)
                else:
                    bindShape(BLOCKS, BLOCK_COLORS, shape)
                    shape = tetromino()
                    endTurn()

            if event.key == pygame.K_SPACE:
                tmpY = shape.getPosY()
                while canBeMoved(BLOCKS, shape.getShape(), shape.getPosX(), tmpY):
                    tmpY += 1
                shape.setPosY(tmpY-1)

            if event.key == pygame.K_g:
                autoDrop()

            if event.key == pygame.K_t:
                print(getEmptyBlocksBelowTallest(BLOCKS))
                

        if event.type == pygame.USEREVENT:
            if canBeMoved(BLOCKS, shape.getShape(), shape.getPosX(), shape.getPosY() + 1):
                shape.setPosY(shape.getPosY() + 1)
            else:
                bindShape(BLOCKS, BLOCK_COLORS, shape)
                shape = tetromino()

    v_zeros = [0 for i in range(B_WIDTH)]

    if BLOCKS[3] == v_zeros:
        autoDrop()


    drawBoard(BLOCKS, BLOCK_COLORS)

    drawShape(shape.posx, shape.posy, shape.getShape(), shape.color, screen)
    
    pygame.display.flip()