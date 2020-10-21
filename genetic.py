from autoplay import *
from utils import *
import math
import random
import numpy as np
import multiprocessing
import threading
import time

NUM_COEFS = 8

def createPopulation(size):
    coefs = [[random.random()*10 for i in range(NUM_COEFS)] for i in range(size)]
    pop = [autoplay(c) for c in coefs]

    return pop

def runPopulation(pop):
    scores = []
    bstart = time.time()
    for p in range(len(pop)):
        start = time.time()
        s = pop[p].play()
        scores.append(s)
        print(p+1,"/", len(pop), "SCORE: ", s, "TIME: ", time.time()-start, " seconds")

    print("Batch done in ", time.time() - bstart, " seconds")
    return scores

def runSingle(a, r):
    s = a.play()
    r.value = s

def runSingleReturn(a):
    s = a.play()
    return s

def runPopulationParalel(pop, th, log):
    start = time.time()
    scores = []
    count = 0

    if __name__ == '__main__':
        procs = []
        results = []
        for p in pop:
            results.append(multiprocessing.Value('d', 0.0))
            procs.append(multiprocessing.Process(target=runSingle, args=(p, results[-1])))

        for p in range(len(procs)):
            log.info("Starting process {0}".format(p))
            p.start()
        
        for p in range(len(procs)):
            p.join()
            log.info("Process {0} finished with score {1}".format(p, results[p].value))

        scores = [r.value for r in results]



    log.info("Batch done in: {0} seconds".format(time.time() - start))
    return scores

def getTopFromPopulation(pop, scores, number):
    indexes = np.argsort(scores)

    top = [pop[i] for i in indexes[-number:]]
    return top

def generateWithCrosover(parents, numChildren):
    sample = []
    children = []
    for n in range(numChildren):
        p1 = random.randint(0, len(parents)-1)
        p2 = random.randint(0, len(parents)-1)

        # childCoefs = parents[p1].getCoefs()

        # for c in range(len(childCoefs)):
        #     if random.randint(0,1) == 0:
        #         childCoefs[c] = parents[p2].getCoefs()[c]
        childCoefs = np.add(parents[p1].getCoefs(), parents[p2].getCoefs())/2
            

        children.append(autoplay(childCoefs))

    mutate(children)

    return children

def generateWithCrossoverProportional(parents, scores, numChildren):
    sampleSpace = 1000
    samples = []
    sumScores = sum(scores)

    for p in range(len(parents)):
        for i in range(math.floor((scores[p] / sumScores) * sampleSpace)):
            samples.append(p)

    children = []

    for c in range(numChildren):
        p1 = random.randint(0,len(samples)-1)
        p2 = random.randint(0,len(samples)-1)


        childCoefs = np.add(parents[samples[p1]].getCoefs(), parents[samples[p2]].getCoefs())/2

        children.append(autoplay(childCoefs))


    return children 


def mutate(children):

    for c in range(len(children)):
        tmp = []
        for coef in children[c].getCoefs():
            if random.randint(0, 10) == 0:
                tmp.append(coef + random.uniform(-0.1, 0.1))
            else:
                tmp.append(coef)

        children[c].setCoefs(tmp)





