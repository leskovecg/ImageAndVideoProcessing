import numpy as np
import matplotlib.pyplot as plt
from labvaja1.vaja01 import loadImage
from labvaja6.displayImage import displayImage
from labvaja6.vaja06 import getParameters
from labvaja6.vaja06 import getRadialValue


## 1. NALOGA (dopolnitev funkcije transformImage):
def transformImage(iType, iImage, iDim, iP, iBgr=0, iInterp=0):

    [Y, X] = iImage.shape
    oImage = np.ones((Y, X)) * iBgr

    for y in range(Y):
        for x in range(X):
            pt = np.array([x, y]) * iDim
            if iType == "affine":
                pt = iP @ np.append(pt, 1)
                pt = pt[:2]
            elif iType == "radial":
                U = getRadialValue(pt, iP["orig_pts"])
                pt = np.array([U @ iP["coef"][:, 0], U @ iP["coef"][:, 1]])

            px = pt / iDim
            if iInterp == 0:
               
                px = np.round(px).astype(np.int64)
                if px[0] >= 0 and px[0] < X and px[1] >= 0 and px[1] < Y:
                    oImage[y, x] = iImage[px[1], px[0]]
        
            elif iInterp == 1:
                pt = pt/iDim
                px = np.floor(px).astype(np.int64)
               
                
                if px[0] >= 0 and px[0] < X and px[1] >= 0 and px[1] < Y:  
                    a = abs((px[0]+1) - pt[0])*abs((px[1]+1) - pt[1])
                    b = abs((px[0]+0) - pt[0])*abs((px[1]+1) - pt[1]) 
                    c = abs((px[0]+1) - pt[0])*abs((px[1]+0) - pt[1]) 
                    d = abs((px[0]+0) - pt[0])*abs((px[1]+0) - pt[1]) 

                   
                    sa = iImage[px[1]+0, px[0]+0]
                    sb = iImage[px[1]+0, min(px[0]+1, iImage.shape[1]-1)]
                    sc = iImage[min(px[1]+1, iImage.shape[0]-1), px[0]+0]
                    sd = iImage[min(px[1]+1, iImage.shape[0]-1), min(px[0]+1, iImage.shape[1]-1)]
                    oImage[y, x] = np.floor(sa*a + sb*b + sc*c + sd*d) 
    return oImage

if __name__ == "__main__":
    
    imSize = [256, 512] 
    pxDim = [2, 1]  
    gX = np.arange(imSize[0]) * pxDim[0]
    gY = np.arange(imSize[1]) * pxDim[1]
    bgr = 63
    
    I = loadImage("labvaja6\data\grid-256x512-08bit.raw", imSize, np.uint8)
    
    # afina preslikava
    T_affine = getParameters("affine", scale=[1, 0.8], trans=[0, 0], rot=0, shear=[0.5, 0])
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=bgr)
    displayImage(tI, "Afina 0.red", gX, gY)
   
    # afina preslikava
    T_affine = getParameters("affine", scale=[1, 0.8], trans=[0, 0], rot=0, shear=[0.5, 0])
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=bgr, iInterp=1)
    displayImage(tI, "Afina 1.red", gX, gY)
    


## 2. NALOGA:
if __name__ == "__main__":
    
    I = loadImage("labvaja6\data\lena-256x512-08bit.raw", imSize, np.uint8)
    
    # a)
    T_affine = getParameters("affine", scale=[0.7, 1.4], trans=[0, 0], rot=0, shear=[0, 0])
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=bgr, iInterp=1)
    displayImage(tI, "Afina 1.red", gX, gY)
    
    # b)
    T_affine = getParameters("affine", scale=[1, 1], trans=[20, -30], rot=0, shear=[0, 0])
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=bgr, iInterp=1)
    displayImage(tI, "Afina 1.red", gX, gY)
    
    # c)
    T_affine = getParameters("affine", scale=[1, 1], trans=[0, 0], rot=-30, shear=[0, 0])
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=bgr, iInterp=1)
    displayImage(tI, "Afina 1.red", gX, gY)
    
    # d)
    T_affine = getParameters("affine", scale=[1, 1], trans=[0, 0], rot=0, shear=[0.1, 0.5])
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=bgr, iInterp=1)
    displayImage(tI, "Afina 1.red", gX, gY)
    
    # e)
    T_affine = getParameters("affine", scale=[1, 1], trans=[-10, 20], rot=15, shear=[0, 0])
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=bgr, iInterp=1)
    displayImage(tI, "Afina 1.red", gX, gY)
    
    # f)
    T_affine = getParameters("affine", scale=[0.7, 0.7], trans=[30, -20], rot=-15, shear=[0, 0])
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=bgr, iInterp=1)
    displayImage(tI, "Afina 1.red", gX, gY)
    

## 3.NALOGA:

# e -- > toga preslikava (rotacija + translacija)
# f -- > podobnostna preslikava (toga preslikava + skaliranje)

## 4.NALOGA:
if __name__ == "__main__":
    I = loadImage("labvaja6\data\lena-256x512-08bit.raw", imSize, np.uint8)
    
    T_affine = getParameters("affine", scale=[1, 1], trans=[0, 0], rot=0, shear=[0, 0])
    T_affine1 = getParameters("affine", scale=[1, 1], trans=[0, 0], rot=-30, shear=[0, 0])
    T_affine2 = getParameters("affine", scale=[1, 1], trans=[0, 0], rot=0, shear=[0.1, 0.5])
    
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=63)
    tI1 = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine1), iBgr=63)
    tI2 = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine2), iBgr=63)
    
    displayImage(tI, "Afina", gX, gY)
    displayImage(tI1, "Afina", gX, gY)
    displayImage(tI2, "Afina", gX, gY)


## 5.NALOGA:
def displayPoints(iXY, iMarker):
    plt.plot(iXY[:, 0], iXY[:, 1], iMarker, ms = 10, lw = 2)

if __name__ == "__main__":
 
    orig_pts = np.array([[0, 0], [511, 0], [0, 511], [511, 511], [63, 63], [63, 447], [447, 63], [447, 447]])
    mapped_pts = np.array([[0, 0], [511, 0], [0, 511], [511, 511], [127, 95], [127, 415], [383, 95], [383, 415]])
    oP = getParameters("radial", orig_pts=orig_pts, mapped_pts=mapped_pts)

    
    I1 = loadImage("labvaja6\data\grid-256x512-08bit.raw", imSize, np.uint8)
    I2 = loadImage("labvaja6\data\lena-256x512-08bit.raw", imSize, np.uint8)
    bgr = 63
    
   
    displayImage(I1, "Originalna slika", gX, gY)
    displayPoints(orig_pts, 'rx')
    rI = transformImage("radial", I1, pxDim, iP=oP, iBgr=bgr)
    displayImage(rI, "Radialna", gX, gY)
    displayPoints(mapped_pts, 'bo')


    displayImage(I2, "Originalna slika", gX, gY)
    displayPoints(orig_pts, 'rx')
    rI = transformImage("radial", I2, pxDim, iP=oP, iBgr=bgr)
    displayImage(rI, "Radialna", gX, gY)
    displayPoints(mapped_pts, 'bo')
# preslikava nedeluje pravilno