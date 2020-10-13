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
        [[1,1],[1,1]],
        [[1,1],[1,1]],
        [[1,1],[1,1]],
        [[1,1],[1,1]]
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
        self.color = self.colors[random.randint(0, len(self.colors)-1)]
        self.shape = self.getRandomShape()
        # self.shape = self.I_shape

    def getRandomShape(self):
        return self.shapes[random.randint(0, len(self.shapes) - 1)]
        
    def setRotation(self, r):
        self.rotation = r

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
    