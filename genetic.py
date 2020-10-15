from autoplay import *
from utils import *
import random
import numpy as np
import multiprocessing

NUM_COEFS = 4

def createPopulation(size):
    coefs = [[random.random()*10 for i in range(NUM_COEFS)] for i in range(size)]
    pop = [autoplay(c) for c in coefs]

    return pop

def runPopulation(pop):
    scores = []
    for p in range(len(pop)):
        scores.append(pop[p].play())
        print(p,"/", len(pop))
    return scores

def runSingle(a):
    return a.play()

def runPopulationParalell(pop):
    pool = multiprocessing.Pool()
    scores = pool.map(runSingle, pop)
    return scores

def getTopFromPopulation(pop, scores, number):
    indexes = np.argsort(scores)

    top = [pop[i] for i in indexes[:number]]
    return top

def generateWithCrosover(parents, numChildren):
    children = []
    for n in range(numChildren):
        p1 = random.randint(0, len(parents)-1)
        p2 = random.randint(0, len(parents)-1)

        childCoefs = np.add(parents[p1].getCoefs(), parents[p2].getCoefs())/2
        children.append(autoplay(childCoefs))

    return children




