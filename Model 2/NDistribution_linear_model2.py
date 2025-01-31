from libraries.IO import readData
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.filters as fl
import math

numHorSec = 48
noBins = 50
bins = np.linspace(100,1000,noBins+1) #divide N scale
horSec = np.linspace(2,10,numHorSec)    #divide Lmax scale
Z = []    #no.hits 2D array - we draw this

horSec = np.linspace(2,10,numHorSec)

for fileNo in horSec:
    if fileNo:
        array = readData("/inf"+str(fileNo))
    #array = readData("/inf_lognormal_"+str(fileNo))
    #array = readData("/inf_loguni_"+str(fileNo))
    #array = readData("/inf_uni_"+str(fileNo))
        Z+=array

Z = [10**min(i, 4) for i in Z]

nV, binsV, patchesV = plt.hist(Z, bins)

out = fl.gaussian_filter(nV, 2)

m = np.where(out == out.max())
m1 = binsV[m][0]

avg = sum(Z)/len(Z)

print('Največja verjetnost: N = '+ str(m1))
print("Povprečje: N = "+str(avg))
plt.cla()
plt.plot(binsV[0:-1], out,'red')
plt.ylabel('frequency')
plt.xlabel('N')
#plt.legend(loc=1)
plt.title('Uniform distribution for L')
#plt.annotate('max', (m1, 0), annotation_clip=False)
#plt.axvline(m1, color ='r', alpha = 0.5)
#plt.axvline(avg, color='r', alpha=0.7)
plt.show()