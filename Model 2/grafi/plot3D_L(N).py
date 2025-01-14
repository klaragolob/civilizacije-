from libraries.IO import readData
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage.filters as fl
from libraries.StandardizeDistribution import StandardizeDistributionW

numHorSec = 48
#numHorSec = 5
noBins = 60
bins = np.linspace(-3, 12, noBins + 1)
horSec = np.linspace(0, 4, numHorSec)
Z = [None] * numHorSec
W = []
i = 0

for fileNo in horSec:
    array = readData("inf" + str(fileNo))
    Z[i], _ = np.histogram(array, bins)
    # Z[i] = np.multiply(Z[i], 2.0/float(fileNo), out=Z[i], casting="unsafe")    # decay factor is 2/fileNo = 2/maxL
    #print(np.argmax(Z[0]))
    print(str(int(10 ** fileNo)) + " - " + str(bins[np.argmax(Z[i])]))
    i += 1
    V, bins = np.histogram(array, bins=bins)
    V = V/max(V)
    W.append(V)
    
    
X, Y = np.meshgrid(bins[0:-1], horSec)





fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)
W = np.array(W)


# Plot the surface
ax.plot_surface(X, Y, W, cmap=cm.coolwarm, shade=True, color='b', alpha=0.8)

ax.set_xlabel("log(L)")
ax.set_ylabel("log(N)")
ax.set_zlabel("Relative probability")
plt.show()

print("done")
