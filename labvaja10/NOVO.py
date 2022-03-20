import numpy as np 
import matplotlib.pyplot as plt
from labvaja1.vaja01 import loadImage
from labvaja1.displayImage import displayImage
from labvaja10.vaja10 import computeDFT2, analyzeDFT2

## 1. NALOGA:
def getFilterSpectrum (iMatrix, iD0, iType):

    # inicializacija - po defaultu frekvence ne supustimo (z 0)
    oMatrix = np.array(iMatrix) * 0

    N, M = iMatrix.shape
    
    # BLPF @ BHPF
    q = 2
    if iType == 'BLPF':
        for n in range(N):
            for m in range(M):
                D = np.sqrt((m + 1 - M / 2)**2 + (n + 1 - N / 2)**2)
                oMatrix[n, m] = 1 / (1 + (D / iD0)**(2 * q))
    if iType == 'BHPF':
        for n in range(N):
            for m in range(M):
                D = np.sqrt((m + 1 - M / 2)**2 + (n + 1 - N / 2)**2)
                oMatrix[n, m] = 1 / (1 + (D / iD0)**(2 * q))
        
        oMatrix = 1 - oMatrix
        
  
    return oMatrix



## 2. NALOGA: 
if __name__ == '__main__':
    
    g = loadImage('labvaja10\data\pattern-236x330-08bit.raw', [236, 330], np.uint8)
    G = computeDFT2(g, iDir='forward')
    gR = computeDFT2(G, iDir='inverse')

    
    # BLPF & BHPF (1/16)
    BL16 = getFilterSpectrum(G, min(G.shape) / 16, 'BLPF')
    analyzeDFT2(BL16, iOperations=['scale', 'display'], iTitle='BLPF (1/16)')
    BH16 = getFilterSpectrum(G, min(G.shape) / 16, 'BHPF')
    analyzeDFT2(BH16, iOperations=['scale', 'display'], iTitle='BHPF (1/16)')
    
    Gf = G * analyzeDFT2(BL16, iOperations=['center'])
    gf = computeDFT2(Gf,'inverse')
    analyzeDFT2(gf, iOperations=['amplitude', 'display'], iTitle='Rekonstruirana slika za BL16')
    Gf = G * analyzeDFT2(BH16, iOperations=['center'])
    gf = computeDFT2(Gf,'inverse')
    analyzeDFT2(gf, iOperations=['amplitude', 'display'], iTitle='Rekonstruirana slika za BH16')
    
    
    
    # BLPF & BHPF (1/4)
    BL4 = getFilterSpectrum(G, min(G.shape) / 4, 'BLPF')
    analyzeDFT2(BL4, iOperations=['scale', 'display'], iTitle='BLPF (1/4)')
    BH4 = getFilterSpectrum(G, min(G.shape) / 4, 'BHPF')
    analyzeDFT2(BH4, iOperations=['scale', 'display'], iTitle='BHPF (1/4)')
    
    Gf = G * analyzeDFT2(BL4, iOperations=['center'])
    gf = computeDFT2(Gf,'inverse')
    analyzeDFT2(gf, iOperations=['amplitude', 'display'], iTitle='Rekonstruirana slika za BL4')
    Gf = G * analyzeDFT2(BH4, iOperations=['center'])
    gf = computeDFT2(Gf,'inverse')
    analyzeDFT2(gf, iOperations=['amplitude', 'display'], iTitle='Rekonstruirana slika za BH4')
    
    
    
    # BLPF & BHPF (1/3)
    BL3 = getFilterSpectrum(G, min(G.shape) / 3, 'BLPF')
    analyzeDFT2(BL3, iOperations=['scale', 'display'], iTitle='BLPF (1/3)')
    BH3 = getFilterSpectrum(G, min(G.shape) / 3, 'BHPF')
    analyzeDFT2(BH3, iOperations=['scale', 'display'], iTitle='BHPF (1/3)')
    
    Gf = G * analyzeDFT2(BL3, iOperations=['center'])
    gf = computeDFT2(Gf,'inverse')
    analyzeDFT2(gf, iOperations=['amplitude', 'display'], iTitle='Rekonstruirana slika za BL3')
    Gf = G * analyzeDFT2(BH3, iOperations=['center'])
    gf = computeDFT2(Gf,'inverse')
    analyzeDFT2(gf, iOperations=['amplitude', 'display'], iTitle='Rekonstruirana slika za BH3')
    
    
    
## 3. NALOGA:
def dokaz(matrika, spekter):

    N, M = matrika.shape
    povprecje = 0 

    for u in range(N):
        for v in range(M):
            povprecje += matrika[u,v] / (N * M) 
    
    if  int(np.real(spekter[0,0])) == int(povprecje * np.sqrt(M*N)):
        print("Dokaz je uspel za sliko!")
    else:
        print("Dokaz ni uspel!")
        


if __name__ == '__main__':
    pattern = loadImage('labvaja10\data\pattern-236x330-08bit.raw', [236, 330], np.uint8)
    displayImage(pattern, 'pattern')
    spekter_pattern = computeDFT2(pattern, iDir='forward')
    
    man = loadImage('labvaja10\data\cameraman-256x256-08bit.raw', [256, 256], np.uint8)
    displayImage(man, 'cameraman')
    spekter_man = computeDFT2(man, iDir='forward')
    
    pumpkin = loadImage('labvaja10\data\pumpkin-200x152-08bit.raw', [200, 152], np.uint8)
    displayImage(pumpkin, 'pumpkin')
    spekter_pumpkin = computeDFT2(pumpkin, iDir='forward')
    
    dokaz(pattern, spekter_pattern)
    dokaz(man, spekter_man)
    dokaz(pumpkin, spekter_pumpkin)