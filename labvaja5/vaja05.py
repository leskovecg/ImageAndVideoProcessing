import numpy as np
import matplotlib.pyplot as plt
from labvaja1.vaja01 import loadImage
from labvaja1.vaja01 import displayImage


def displayImage (iImage, iTitle, iGridX=None, iGridY=None):
    plt.figure()
    plt.title(iTitle)

    if iGridX is not None and iGridY is not None:
        stepX = iGridX[1] - iGridX[0]
        stepY = iGridY[1] - iGridY[0]
        extent = (
            iGridX[0] - 0.5*stepX,
            iGridX[-1] + 0.5*stepX,
            iGridY[-1] + 0.5*stepY,
            iGridY[0] - 0.5*stepY,
        )
    else:
        extent = (
            0 - 0.5,
            iImage.shape[1] - 0.5,
            iImage.shape[0] -0.5,
            0 - 0.5,
        ) 
    plt.imshow(
        iImage, 
        cmap=plt.cm.gray, 
        vmin=0, 
        vmax=255, 
        aspect='equal', 
        extent=extent
    )
    plt.show()


# 1. Naloga:
if __name__ == '__main__':
    I = loadImage('labvaja5\data\image-512x512-16bit.raw',[512, 512], np.int16)
    displayImage(I, 'Originalna slika')
    print(f'Min: {I.min()}, maks vrednost: {I.max()}')
    
    
    
# 2. Naloga:
def scaleImage (iImage, iA, iB):
    
    # inicializacija izhodne slike
    oImage = np.array(iImage, dtype=float)
    
    # linearna preslikava:
    oImage = iImage*iA + iB
    
    
    return oImage
    
if __name__ == '__main__':
    sI = scaleImage(I, -0.125, 256)
    displayImage(sI, 'Slika po splošni lin. preslikavi')
    print(f'Min: {sI.min()}, maks vrednost: {sI.max()}')
    
    
    
# 3. Naloga:
def windowImage(iImage, iC, iW):
    
    #iW - dolžina okna
    #f - vhodna slika

    # okno:
    oImage = 255/iW*(np.array(iImage) - (iC - iW/2))
    
    # levi del:
    oImage[iImage < (iC - iW/2)] = 0
    
    # desni del:
    oImage[iImage > (iC + iW/2)] = 255
    
    return oImage

if __name__ == '__main__':
    wI = windowImage(sI, 1000, 500)
    displayImage(wI, 'Slika po linearnem oknjenju')
    print(f'Min: {wI.min()}, maks vrednost: {wI.max()}')
    

# 4. Naloga:
def sectionalScaleImage (iImage, iS, oS):

    # oS --> y os
    # iS --> x os
    
    # sg --> oS
    # sf --> iS
    
    oImage = np.array(iImage, dtype = float)
    
    for i in range(len(iS) - 1):
        sL = iS[i]
        sH = iS[i+1]
        # preverjanje, če uporabnik zamenja 
        if sL > sH:
            sL = iS[i+1]
            sH = iS[i] 
    
        mask = np.logical_and(iImage >= sL, iImage <= sH) 
        
        k = (oS[i+1] - oS[i])/(iS[i+1]-iS[i])
        oImage[mask] = k*(iImage[mask] - iS[i]) + oS[i] 
    
    return oImage

if __name__ == '__main__':
    
    """
    primerjava med lin. onkjjenje in slika po odsekoma lin. preslikavi:
    prej kar je blo prej črno je šlo na temno sivo(iz 85 je šlo na temno)
    prej svetlo --> sivkasto, svetlejš sivkasto
    bela --> zelo svetla bela  
    """
    ssI = sectionalScaleImage(wI, [0, 85, 170, 255], [85, 0, 255, 170])
    displayImage(ssI, 'Slika po odsekoma lin. preslikavi')
    print(f'Min: {ssI.min()}, maks vrednost: {ssI.max()}')
    
    
    
# 5. Naloga:
def gammaImage (iImage, iG):
    # gama preslikava 
    oImage = 255**(1-iG)*(np.array(iImage)**iG)

    return oImage


if __name__ == '__main__':

    gI = gammaImage(wI, 0.5)
    displayImage(gI, 'Slika po gama preslikavi:')
    print(f'Min: {gI.min()}, maks vrednost: {gI.max()}')
    
    
    """prim. z lin oknjenjem in zdajšnjo:
    gamma --> vse intenzitete svetlejše, večji kontrast
    
    
    """
    
    
 
# poročilo   
# 1.naloga -
# 2.naloga:
def thresholdImage (iImage, iT):

    # inicializacija izhodne slike
    oImage = np.array(iImage, dtype=float)
    
    # levi del:
    oImage[iImage <= iT] = 0
    
    # desni del:
    oImage[iImage > iT] = 255
    
    return oImage

if __name__ == '__main__':
    uI = thresholdImage(wI, 127)
    displayImage(uI, 'Slika po upragovanju sivinskih vrednosti')
    print(f'Min: {uI.min()}, maks vrednost: {uI.max()}')
    
# 3.naloga:-

"""
# 4.naloga:
def nonLinearSectionalScaleImage (iImage, iS, oS):

    oImage = np.array(iImage, dtype = float)
    
    for i in range(len(iS) - 1):
        sL = iS[i]
        sH = iS[i+2]
        # preverjanje, če uporabnik zamenja 
        if sL > sH:
            sL = iS[i+2]
            sH = iS[i] 
    
        mask = np.logical_and(iImage >= sL, iImage <= sH) 
        
        oImage[mask] = A[i]*iImage[mask]**2 + B[i]*iImage[mask] + C[i]
        
    return oImage

if __name__ == '__main__':
  
    nssI = nonLinearSectionalScaleImage(wI, [0, 40, 80, 127, 167, 207, 255], [0, 255, 80, 20, 167, 240, 255])
    displayImage(nssI, 'Slika po odsekoma nelin. preslikavi')
    print(f'Min: {nssI.min()}, maks vrednost: {ssI.max()}')
""" 
    