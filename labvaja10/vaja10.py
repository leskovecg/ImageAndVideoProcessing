import numpy as np 
import matplotlib.pyplot as plt
from labvaja1.vaja01 import loadImage
from labvaja1.displayImage import displayImage

## 1. NALOGA:
if __name__ == '__main__':
    g = loadImage('labvaja10\data\pattern-236x330-08bit.raw', [236, 330], np.uint8)
    displayImage(g, 'Originalna slika')
    
    
    
## 2. NALOGA:
def computeDFT2 (iMatrix, iDir='forward'):
    """
Funkcija za računanje 2D DFT oz. 2D IDFT
"""
    N, M = iMatrix.shape
    # preoblikujemo v matriko ki ima eno vrstico in neki stolpcev
    n = np.arange(0, N).reshape(1, -1)
    m = np.arange(0, M).reshape(1, -1)
    
    WN = 1/np.sqrt(N) * np.exp(-1j*2*np.pi/N)**(n.T@n)
    WM = 1/np.sqrt(M) * np.exp(-1j*2*np.pi/M)**(m.T@m)
    
    if iDir == 'inverse':
        WN = np.conj(WN)
        WM = np.conj(WM)
        
    
    oMatrix = WN @ iMatrix @ WM

    return oMatrix

if __name__ == '__main__':
    G = computeDFT2(g, iDir='forward')
    gR = computeDFT2(G, iDir='inverse')
    # pričakujemo lahko enaki sliki:
    displayImage(g, 'Originalna slika')
    displayImage(gR.real,'rekonstruirana slika')
    
    

## 3. NALOGA:
def analyzeDFT2 (iMatrix, iOperations, iTitle =""):
    """
Funkcija za analizo 2D DFT spektra
"""
    # inicializacija
    oMatrix = np.array(iMatrix)

    # zanka čez vse operacije:
    for operation in iOperations:
        # amplitudni spekter
        if operation == "amplitude":
            oMatrix = np.abs(oMatrix)
        elif operation == 'phase':
            oMatrix = np.unwrap(np.angle(oMatrix))
        elif operation == 'ln':
            oMatrix = np.log(oMatrix + 1e-10)
        elif operation == 'log':
            oMatrix = np.log10(oMatrix + 1e-10)
        elif operation == 'scale':
            lim = [oMatrix.min(), oMatrix.max()]
            oMatrix = (oMatrix - lim[0]) / (lim[1] - lim[0])*255
            oMatrix = oMatrix.astype(np.uint8)
        elif operation == 'center':
            N, M = oMatrix.shape
            center = np.array([N/2, M/2]).astype(int)
            A = oMatrix[: center[0], : center[1]]
            B = oMatrix[center[0] :, : center[1]]
            C = oMatrix[center[0] :, center[1] :]
            D = oMatrix[: center[0], center[1] :]
            upper = np.hstack((C, B))
            lower = np.hstack((D, A))
            oMatrix = np.vstack((upper, lower))
        elif operation == 'display':
            plt.figure()
            plt.imshow(oMatrix, aspect='equal', cmap=plt.cm.gray)
            plt.title(iTitle)
        else: 
            raise NotImplementedError
            
    return oMatrix
    
if __name__ == '__main__':
    analyzeDFT2(G, iOperations=['amplitude', 'center', 'log', 'scale', 'display'], iTitle="A (log)")
    analyzeDFT2(G, iOperations=['phase', 'scale', 'display'], iTitle="F")
    
    
    
## 4. NALOGA:
def getFilterSpectrum (iMatrix, iD0, iType):
    """
Funkcija za določanje 2D spektra izbranega idealnega
nizkoprepustnega (ILPF) ali visokoprepustnega (IHPF) filtra
"""
    # inicializacija - po defaultu frekvence ne supustimo (z 0)
    oMatrix = np.array(iMatrix) * 0

    N, M = iMatrix.shape
    
    # idealni nizkopasovni filter - ILPF
    if iType[0] == 'I':
        for n in range(N):
            for m in range(M):
                D = np.sqrt((m + 1 - M / 2)**2 + (n + 1 - N / 2)**2)
                if D <= iD0:
                    oMatrix[n, m] = 1
    if iType[1:] == 'HPF':
        oMatrix = 1 - oMatrix
            
    return oMatrix
    
if __name__ == '__main__':
    H = getFilterSpectrum(G, min(G.shape) / 16, 'ILPF')
    analyzeDFT2(H, iOperations=['scale', 'display'], iTitle='H')
    
    H1 = getFilterSpectrum(G, min(G.shape) / 16, 'IHPF')
    analyzeDFT2(H1, iOperations=['scale', 'display'], iTitle='H1')
    
    Gf = G * analyzeDFT2(H, iOperations=['center'])
    gf = computeDFT2(Gf,'inverse')
    analyzeDFT2(gf, iOperations=['amplitude', 'display'])