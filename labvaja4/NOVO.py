import numpy as np
import matplotlib.pyplot as plt
#from labvaja3.vaja03 import displayImage

## 1. NALOGA (nalaganje 3D slike):
def loadImage3D(iPath, iSize, iType):
    
    fid = open(iPath, 'rb')
    im_shape = (iSize[1], iSize[0], iSize[2])

    oImage = np.ndarray(shape=im_shape, dtype=iType, buffer=fid.read(), order='F')

    fid.close()
    return oImage

if __name__ == '__main__':

    imSize = [512, 58, 907]
    pxDim = [0.597656, 3, 0.597656]

    I = loadImage3D('labvaja4\data\spine-512x058x907-08bit.raw', imSize, np.uint8)
    print(I.shape)



## 2.NALOGA (prerez):
def getPlanarCrossSection (iImage, iDim, iNormVec, iLoc):

    oCS = []
    oV = []
    oH = []

    im_shape = iImage.shape

    # stranski prerez (nx = (1, 0, 0)):
    if iNormVec == [1, 0, 0]:
        oCS = iImage[:, iLoc, :].T 
        oV = np.arange(im_shape[2])*iDim[2] 
        oH = np.arange(im_shape[0])*iDim[1] 
    # čelni prerez (ny = (0, 1, 0)):
    elif iNormVec == [0, 1, 0]:
        oCS = iImage[iLoc, :, :].T
        oV = np.arange(im_shape[2])*iDim[2] 
        oH = np.arange(im_shape[1])*iDim[0]
    # prečni prerez (nz = (0, 0, 1)):
    elif iNormVec == [0, 0, 1]:
        oCS = iImage[:, :, iLoc]
        oV = np.arange(im_shape[0])*iDim[1] 
        oH = np.arange(im_shape[1])*iDim[0]
    return oCS, oH, oV

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

if __name__ == '__main__':
    xc = 256
    [xCS, xH, xV] = getPlanarCrossSection(I, pxDim, [1, 0, 0], xc)
    displayImage(xCS,'Stranski pravokotni ravninski prerez:',xH,xV)

    yc = 35
    [yCS, yH, yV] = getPlanarCrossSection(I, pxDim, [0, 1, 0], yc)
    displayImage(yCS,'Čelni pravokotni ravninski prerez:',yH,yV)

    zc = 467
    [zCS, zH, zV] = getPlanarCrossSection(I, pxDim, [0, 0, 1], zc)
    displayImage(zCS,'Prečni pravokotni ravninski prerez:',zH,zV)



## 3.NALOGA (projekcija):
def getPlanarProjection (iImage, iDim, iNormVec, iFunc):

    oP = []
    oV = []
    oH = []

    [Y, X, Z] = iImage.shape

    # stranska projekcija (nx = (1, 0, 0))
    if iNormVec == [1, 0, 0]:
        oH = np.arange(Y)*iDim[1]
        oV = np.arange(Z)*iDim[2]

        # dolgi način:
        oP = np.zeros((Z, Y))
        for z in range(Z):
            for y in range(Y):
                oP[z, y] = iFunc(iImage[y, :, z])
        
        # krajši način:
        #oP = iFunc(iImage, axis=1).T

    # čelna projekcija (ny = (0, 1, 0))
    elif iNormVec == [0, 1, 0]:
        oH = np.arange(X)*iDim[0]
        oV = np.arange(Z)*iDim[2]
        
        # dolgi način:
        oP = np.zeros((Z, X))
        for z in range(Z):
            for x in range(X):
                oP[z, x] = iFunc(iImage[:, x, z])
        
        
        # krajši način:
        #oP = iFunc(iImage, axis=0).T

    # prečna projekcija (nz = (0, 0, 1))
    elif iNormVec == [0, 0, 1]:
        oH = np.arange(X)*iDim[0]
        oV = np.arange(Y)*iDim[1]

        oP = iFunc(iImage, axis=2)
    
    # čelna poševna ravninska projekcija (nxy = (x, y, 0))
    elif iNormVec[2] == 0:
        
        """
        n1 = [0,1,0]
        n2 = iNormVec
        kot = np.arccos((n1[0]*n2[0] + n1[1]*n2[1] + n1[2]*n2[2]) / ((np.sqrt(n1[0]**2 + n1[1]**2 + n1[2]**2))*(np.sqrt(n2[0]**2 + n2[1]**2 + n2[2]**2))))
        
        for x in range(X):
            for y in range(Y):
                
                stara_tocka = [x, y]
                x_nov = x*np.cos(kot) - y*np.sin(kot)
                y_nov = x*np.sin(kot) + y*np.cos(kot)
                nova_tocka = [x_nov, y_nov]
                oP[z, x] = iFunc(iImage[y_nov, x_nov, z])
                
        oH = np.arange(X)*iDim[0]
        oV = np.arange(Z)*iDim[2]
        """
    return oP, oH, oV

if __name__ == '__main__':
    
    func = np.max

    [xP, xH, xV] = getPlanarProjection(I, pxDim, [1,0,0], func) 
    displayImage(xP, 'Stranska pravokotna ravninska projekcija:', xH, xV)

    [yP, yH, yV] = getPlanarProjection(I, pxDim, [0,1,0], func) 
    displayImage(yP, 'Čelna pravokotna ravninska projekcija:', yH, yV)

    [zP, zH, zV] = getPlanarProjection(I, pxDim, [0,0,1], func) 
    displayImage(zP, 'Prečna pravokotna ravninska projekcija:', zH, zV)
    
    
    # za poševno ravn. projek.:
    # 1.normala:
    [xyP, xyH, xyV] = getPlanarProjection(I, pxDim, [3.83,9.24,0], func) 
    #displayImage(xyP, 'Čelna poševna ravninska projekcija:', xyH, xyV)
    
    # 2.normala:
    #[xyP, xyH, xyV] = getPlanarProjection(I, pxDim, [1,1,0], func) 
    #displayImage(xyP, 'Čelna poševna ravninska projekcija:', xyH, xyV)
    
    # 3.normala:
    #[xyP, xyH, xyV] = getPlanarProjection(I, pxDim, [9.24,3.83,0], func) 
    #displayImage(xyP, 'Čelna poševna ravninska projekcija:', xyH, xyV)




    func = np.mean

    [xP, xH, xV] = getPlanarProjection(I, pxDim, [1,0,0], func) 
    displayImage(xP, 'Stranska pravokotna ravninska projekcija:', xH, xV)

    [yP, yH, yV] = getPlanarProjection(I, pxDim, [0,1,0], func) 
    displayImage(yP, 'Čelna pravokotna ravninska projekcija:', yH, yV)

    [zP, zH, zV] = getPlanarProjection(I, pxDim, [0,0,1], func) 
    displayImage(zP, 'Prečna pravokotna ravninska projekcija:', zH, zV)
    
  
    