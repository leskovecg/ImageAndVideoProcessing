import numpy as np
import matplotlib.pyplot as plt
from labvaja1.displayImage import displayImage
import cv2

## 1. NALOGA:
def loadFrame(iVideo, iK):
    """
Funkcija za nalaganje slike iz videa
"""
    # postavi reader na (iK -1)-ti frame
    iVideo.set(1, iK-1)
    ret, oFrame = iVideo.read()
    # vrstice (100), stolpce (160), vzamemo 1.sliko = R (od RGB):
    oFrame = oFrame[:,:,0].astype(float)
    
    return oFrame

if __name__ == '__main__':
    # naloži video
    V1 = cv2.VideoCapture("labvaja11/data/simple-video.avi")
    
    print(f'število slik v videu: {int(V1.get(cv2.CAP_PROP_FRAME_COUNT))}')
    I1 = loadFrame(V1, iK = 30)
    I2 = loadFrame(V1, iK = 31)
    
    displayImage(I1, 'slika 1')
    displayImage(I2, 'slika 2')
    

## 2: NALOGA:    
def framePrediction(iF, iMV):
    iMV = np.array(iMV).astype(int)
    
    # axis = 0 - vrtijo se vrstice, axis = 1 - vrtijo se stolpci
    ## premikamo intenzitete za iMV[1] navzdol in za iMV[0] desno (po mreži)
    oF = np.roll(iF, [iMV[1], iMV[0]], axis=(0,1))
    
    # dx komponenta vektorja:
    if iMV[0] >= 0:
        oF[:, :iMV[0]] = -1
    else:
        oF[:, iMV[0] :] = -1
    
    # dy komponenta vektorja:  
    if iMV[1] >= 0:
        oF[:, :iMV[1]] = -1
    else:
        oF[:, iMV[1] :] = -1
    
    return oF
    

def blockMatching(iF1, iF2, iSize, iSearchSize):
    """
Funkcija za dolocanje polja vektorjev premika z blocnim
ujemanjem
"""
    Y, X = iF1.shape
    
    # želimo ugotoviti št. blokov znotraj slike:
    M = int(X / iSize[0])
    N = int(Y / iSize[1])
    
    # inicializacija vektorjev premika
    oMF = np.zeros((N, M, 2), dtype=float)
    oCP = np.zeros((N, M, 2), dtype=float)
    Err = np.ones((N, M), dtype=float)*255
    
    # inicializacija logaritemskega iskanja vektorja premika 
    P = (iSearchSize - 1) / 2
    PTS = np.array([[0,0], [1,0], [-1,0], [0,1], [0,-1], [1,1], [-1,1], [1,-1], [-1,-1]])
    
    # zanka čez vse bloke
    for n in range(N):
        y_min = n*iSize[1]
        y_max = (n+1)*iSize[1]
        y = np.arange(y_min, y_max)
        for m in range(M):
            x_min = m*iSize[0]
            x_max = (m+1)*iSize[0]
            x = np.arange(x_min, x_max)
            
            # središče trenutnega bloka
            oCP[n,m,0] =x.mean() 
            oCP[n,m,1] =y.mean()
            
            # prvi blok vrži ven:
            B1 = iF1[y_min:y_max, x_min:x_max]
            B2 = iF2[y_min:y_max, x_min:x_max]  
            
            for i in range(1, 4):
                Pi = (P + 1) / (2 ** i)
                PTSi = PTS * Pi
                
                d0 = np.array([oMF[n,m,0], oMF[n,m,1]])
                
                for p in range(PTSi.shape[0]):
                    # trenutni vektor premika
                    d = d0 + PTSi[p, :]
                    
                    # napovedan F2 na podlagi F1 in vektorja premika
                    pF2 = framePrediction(iF1, d)
                    # napovedan blok dva izločimo iz napovedane slicice 2
                    pB2 = pF2[y_min:y_max, x_min:x_max]
                    
                    idx = np.logical_and(B2 >= 0, pB2 >= 0)
                    
                    bErr = np.sum(np.abs(B2[idx] - pB2[idx])) / idx.sum()
                    
                    if bErr < Err[n, m]:
                        Err[n, m] = bErr
                        oMF[n, m, :] = d
                        
                    
    return oMF, oCP

if __name__ == '__main__':
    
    bsize = [8, 8]
    searchSize = 15
    MF, CP = blockMatching(I1, I2, bsize, searchSize)
    
    
## 3. NALOGA:
from labvaja11.displayImage import displayImage
    
def displayMotionField(iMF, iCP, iTitle, iImage = None):
    """
Funkcija za prikaz polja vektorjev premika
"""
    if iImage is None:
        fig = plt.figure()
        plt.gca().invert_yaxis()
        plt.gca().set_aspect("equal")
        plt.title(iTitle)
    else:
        fig = displayImage(iImage, iTitle=iTitle, show = False)
    
    plt.quiver(iCP[:,:,0], iCP[:,:,1], iMF[:,:,0], iMF[:,:,1], color='red', scale=0.5, units='xy', angles='xy')
    
    return fig
    
if __name__ == '__main__':
    displayMotionField(MF, CP, iTitle='Vektorji premika')
    displayMotionField(MF, CP, iTitle='Superponirani vektorji premika', iImage = I1)
    
    



