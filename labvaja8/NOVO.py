import numpy as np
from labvaja1.vaja01 import loadImage
from labvaja1.displayImage import displayImage

## 5.NALOGA:

## a)
from labvaja5.vaja05 import scaleImage
from labvaja7.vaja07 import spatialFiltering

if __name__ == "__main__":
    imSize = [160, 160]  # x, y
    pxDim = [1, 1]  # dx, dy
    gX = np.arange(imSize[0]) * pxDim[0]
    gY = np.arange(imSize[1]) * pxDim[1]
    I = loadImage("labvaja8\data\circles-160x160-08bit.raw", imSize, np.uint8)
    displayImage(I, "Originalna slika", gX, gY)
    print(f'Min: {I.min()}, maks vrednost: {I.max()}')
    
    
    K1 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kI1 = spatialFiltering("kernel", iImage=I, iFilter=K1)
    sI1 = scaleImage(kI1, 255/2040, 1020*255/2040)
    displayImage(sI1, "Sobelov operator za x smer")
    print(f'Min: {sI1.min()}, maks vrednost: {sI1.max()}')
    
    
    K2 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    kI2 = spatialFiltering("kernel", iImage=I, iFilter=K2)
    sI2 = scaleImage(kI2, 255/2040, 1020*255/2040)
    displayImage(sI2, "Sobelov operator za y smer")
    print(f'Min: {sI2.min()}, maks vrednost: {sI2.max()}')
    
    
    kIam = np.sqrt(kI1**2 + kI2**2)
    sIam = scaleImage(kIam, 255/1140.395, 0)
    displayImage(sIam, "Amplitudni odziv")
    print(f'Min: {sIam.min()}, maks vrednost: {sIam.max()}')
    
    
## b)
from labvaja5.vaja05 import thresholdImage

if __name__ == '__main__':
   
    uI = thresholdImage(sIam, 254)
    displayImage(uI, 'Slika po upragovanju sivinskih vrednosti')
    print(f'Min: {uI.min()}, maks vrednost: {uI.max()}')
    

## c) ..
