import numpy as np
import mpmath as mp
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random
import math
import time
from libraries.IO import saveData
from libraries.lifeDist import lifeDist, lifeDist2
from mpmath import mpmathify, mp, mpf

'''''
Model 2: https://arxiv.org/ftp/arxiv/papers/1510/1510.08837.pdf
Using Sandberg distribution

Model 2 opposite to original Drake equation (calculates how many int.civs are out there now), this model caluclates how many int.civs. were ever out there
/to do so.. it does not use L variable and uses total no. of stars in the universe instead of the rate at which the stars are apperaing
/for less known parameters: biotechnicalProbability, the paper calculates minimal threshold and uses different values for that. We use Sandberg
'''''


def sample_value(fromv, tov, dist):
    if dist == "loguniform":
        return random.uniform(fromv, tov)
    elif dist == "uniform":
        return np.log10(np.random.uniform(10 ** fromv, 10 ** tov))
    elif dist == "halfgauss":
        sigmaHalfGauss = (
                                 10 ** tov - 10 ** fromv) / 3  # /3 je tako da bo 3sigma cez cel interval
        return np.log10(np.abs(np.random.normal(0, sigmaHalfGauss)) + 10 ** fromv)  # gauss
    elif dist == "lognormal":
        median = (tov - fromv) / 2 + tov  # polovica intervala
        sigma = (median - tov) / 3  # tako, da je 3sigma cez cel obseg
        return np.random.normal(median, sigma)  # lognormal
    return tov


# Generate a point
def getPoint(maxN=10):
    dist = "uniform"
    RStarSample = sample_value(0, 2, dist)  # logaritmic
    Nstar = 11.4771212547  # total number of stars. Paper persumes there are 2*10^22 oz. 22.30103  in our observable universe - only for our galaxy 3*10^11 oz. 11.4771212547
    fPlanets = sample_value(-1, 0, dist)  # paper suggests 1           np.random.normal(1)
    nEnvironment = sample_value(-1, 0, dist)  # paper suggests 0.2    np.random.normal(0.2)
    astrophysicsProbability2 = np.random.normal(0.155, 0.73)  # distributuin that is similar to the one if we calculate it our self
    if (astrophysicsProbability2 > 2):  # so that the distribution look more similar
        astrophysicsProbability2 = sample_value(1.65, 1.95, dist)
    if (astrophysicsProbability2 < -2):
        astrophysicsProbability2 = sample_value(-1.95, -1.65, dist)

    fInteligence = sample_value(-3, 0, dist)
    fCivilization = sample_value(-2, 0, dist)  # in the paper it is mentioned as ft
    fLife = lifeDist(mean=0, sigma=50)
    fLifeEks = float(mp.log(fLife, 10))

    # L = random.uniform(2, maxL)     #loguniform
    # L = math.log10(sample_value(10 ** 2, 10 ** maxL, dist))  # uniform
    N = sample_value(0, maxN, dist)

    # biotechnicalProbability  - lower bound calcuclated to be 2.5*10^-24   aka -23.60206 - only for our galaxy 	1.7*10^-11 aka -10.76955

    # astrophysicsProbability = RStarSample + fPlanets + nEnvironment  # use Nstar instead of rstarsample if no L
    # biotechnicalProbability = fInteligence + fCivilization + fLifeEks
    biotechnicalProbability = sample_value(-11, -3, dist)
    # resitev = astrophysicsProbability + biotechnicalProbability   #calculates A = number of civ that have ever apperared in the world
    resitev = N - (astrophysicsProbability2 + biotechnicalProbability)  # calculates A = number of civ that have ever apperared in the world

    E3 = Nstar + fPlanets + nEnvironment
    E4 = E3 + fLife
    # E5 = E4 + fInteligence

    # threshold if N values are very 5lohttps://drive.google.com/drive/folders/1KFS5QMfw__qhXwCI_gDg8MtZKCieLpp3?fbclid=IwAR0CHSuTXxmH8Ge9q_NYNA6OsNWjgoI0NSDu-nLymRvLyjv61-xktdF4Fvww
    # if (resitev < 0):       #treshold from min possible solution
    # if (resitev < 0) or (resitev > 5):       #threshold min and L possible solution
    #glajenje = 0.4
    #if resitev < np.random.normal(0, glajenje) or resitev > np.random.normal(5, glajenje):  # bokal?
    #    return False

    # x.append(astrophysicsProbability) #from our distribution calculated distribution
    # y.append(astrophysicsProbability2)  #from our distribution
    return resitev


drawnPoints = 0
numHorSec = 48
noIterationsPerMaxN = 20000
logPoints = np.linspace(0, 4, numHorSec)
allPoints = noIterationsPerMaxN * numHorSec

fixed_n = [0,1,2,3,4]

for maxN in logPoints:
    #for maxN in fixed_n:
    array = []
    for i in range(0, noIterationsPerMaxN):
        point = getPoint(maxN)
        #if type(point) != type(False):
        array.append(point)

    saveData(array, "inf" + str(maxN))
    print("File: inf" + str(maxN) + ".txt created. no of points:" + str(len(array)))
    drawnPoints = drawnPoints + len(array)
    pointFraction = (drawnPoints * 100) / allPoints
print('done')
print('Drawn points: ' + str(drawnPoints) + '  Which is: ' + str(pointFraction) + '%')
