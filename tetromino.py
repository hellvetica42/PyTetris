import random
class tetromino:
    I_shape = [
        [[0,0,0,0],
            [1,1,1,1],
            [0,0,0,0],
            [0,0,0,0]],

        [[0,0,1,0],
            [0,0,1,0],
            [0,0,1,0],
            [0,0,1,0]], 

        [[0,0,0,0],
            [0,0,0,0],
            [1,1,1,1],
            [0,0,0,0]], 

        [[0,1,0,0],
            [0,1,0,0],
            [0,1,0,0],
            [0,1,0,0]]
    ]

    L_shape = [
        [[1,0,0],
         [1,1,1],
         [0,0,0]],

        [[0,1,1],
         [0,1,0],
         [0,1,0]],

        [[0,0,0],
         [1,1,1],
         [0,0,1]],

        [[0,1,0],
         [0,1,0],
         [1,1,0]]
    ]

    J_shape = [
        [[0,0,1],
         [1,1,1],
         [0,0,0]],

        [[0,1,0],
         [0,1,0],
         [0,1,1]],

        [[0,0,0],
         [1,1,1],
         [1,0,0]],

        [[1,1,0],
         [0,1,0],
         [0,1,0]]
    ]

    O_shape = [
        [[1,1],
         [1,1]],

        [[1,1],
         [1,1]],

        [[1,1],
         [1,1]],

        [[1,1],
         [1,1]]
    ]

    S_shape = [
        [[0,1,1],
         [1,1,0],
         [0,0,0]],

        [[0,1,0],
         [0,1,1],
         [0,0,1]],

        [[0,0,0],
         [0,1,1],
         [1,1,0]],

        [[1,0,0],
         [1,1,0],
         [0,1,0]]
    ]

    Z_shape = [
        [[1,1,0],
         [0,1,1],
         [0,0,0]],

        [[0,0,1],
         [0,1,1],
         [0,1,0]],

        [[0,0,0],
         [1,1,0],
         [0,1,1]],

        [[0,1,0],
         [1,1,0],
         [1,0,0]],
    ]

    T_shape = [
        [[0,1,0],
         [1,1,1],
         [0,0,0]],

        [[0,1,0],
         [0,1,1],
         [0,1,0]],

        [[0,0,0],
         [1,1,1],
         [0,1,0]],

        [[0,1,0],
         [1,1,0],
         [0,1,0]]
    ]

    colors = [
        (96, 227, 234),
        (237, 88, 78),
        (78, 237, 91),
        (252, 245, 103)
    ]


    def __init__(self):
        self.rotation = 0
        self.posx, self.posy = 0, 0
        self.shapes = [self.I_shape, self.L_shape, self.J_shape, self.O_shape, self.S_shape, self.Z_shape, self.T_shape]
        self.shapeRotations = [2, 4, 4, 1, 2, 2, 4]
        self.numRotations = 0
        self.color = self.colors[random.randint(0, len(self.colors)-1)]
        self.shape = self.getRandomShape()
        # self.shape = self.I_shape

    def getRandomShape(self):
        tmp = random.randint(0, len(self.shapes) - 1)
        self.numRotations = self.shapeRotations[tmp]
        return self.shapes[tmp]
        
    def setRotation(self, r):
        self.rotation = r

    def getNumRotations(self):
        return self.numRotations

    def getShape(self):
        return self.shape[self.rotation]

    def setPosX(self, x):
        self.posx = x
    
    def getPosX(self):
        return self.posx
    
    def setPosY(self, y):
        self.posy = y

    def getPosY(self):
        return self.posy

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def getRotated(self):
        return self.shape[(self.rotation + 1) % 4]
    