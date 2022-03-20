import numpy as np
import matplotlib.pyplot as plt
#from labvaja3.skripta import displayImage

## 1. NALOGA (nalaganje 3D slike):
def loadImage3D(iPath, iSize, iType):
    
    # rb je binary format for reading
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

    # iDim = (dx, dy, dz)

    im_shape = iImage.shape

    # stranski prerez (nx = (1, 0, 0)):
    if iNormVec == [1, 0, 0]:
        # prvi : --> x pustimo pri miru, tretji : --> z pustimo pri miru
        oCS = iImage[:, iLoc, :].T ## za ležečo sliko tu odstrani transponiranje
        # np.arange(907) -- > vrne array 907 elementov od 0 pa do 906
        # np.arange(907)*0 -- > vrne array 907 elementov samih 0
        # np.arange(907)*0.59 --> vrne array 907 elementov od 0 do 534.54, s korakom po 0.59
        oV = np.arange(im_shape[2])*iDim[2] ## za ležečo sliko pred transponiranjem daj namesto oV oH
        oH = np.arange(im_shape[0])*iDim[1] ## za ležečo sliko pred transponiranjem daj namesto oH oV
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
    #else: # te zakomentiramo, ker smo dodali po if-u še elif
        #NotImplementedError
    return oCS, oH, oV

def displayImage (iImage, iTitle, iGridX=None, iGridY=None):
    # ustvarimo prikazno okno
    plt.figure()
    # zapišemo naslov, ki se pokaže
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
        # prikažemo naloženo sliko na zaslon
        extent = (
            0 - 0.5,
            iImage.shape[1] - 0.5,
            iImage.shape[0] -0.5,
            0 - 0.5,
        ) # lahko tudi dodatno razširimo platno okoli slike, da v priakz vključimo tudi robove
    plt.imshow(
        iImage, 
        cmap=plt.cm.gray, 
        vmin=0, 
        vmax=255, 
        aspect='equal', # poskrbimo, da je širina enaka kot višina slikovnega elementa 
        extent=extent
    )

    # na koncu z urejanjem priakza, kličemo metodo plt.show() za prikaz slike
    plt.show()

if __name__ == '__main__':
    xc = 290
    [xCS, xH, xV] = getPlanarCrossSection(I, pxDim, [1, 0, 0], xc)
    displayImage(xCS,'Stranski pravokotni ravninski prerez:',xH,xV)



## 3.NALOGA (projekcija):
def getPlanarProjection (iImage, iDim, iNormVec, iFunc):

    # inicializacija  vhodnih argumentov 
    oP = []
    oV = []
    oH = []

    # dimenzije slike
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

        oP = iFunc(iImage, axis=0).T

    # prečna projekcija (nz = (0, 0, 1))
    elif iNormVec == [0, 0, 1]:
        oH = np.arange(X)*iDim[0]
        oV = np.arange(Y)*iDim[1]

        oP = iFunc(iImage, axis=2)
        
    elif iNormVec[2] == 0:
        # tu moramo nek napisat
        print("piši")

    #else: # te zakomentiramo, ker smo dodali po if-u še elif
        #NotImplementedError
    return oP, oH, oV

if __name__ == '__main__':
    """
    func = np.max
    [xP, xH, xV] = getPlanarProjection(I, pxDim, [1,0,0], func) 
    displayImage(xP, '', xH, xV)
    """
    """
    func = np.mean
    [xP, xH, xV] = getPlanarProjection(I, pxDim, [1,0,0], func) 
    displayImage(xP, '', xH, xV)
    """
    func = np.median
    [xP, xH, xV] = getPlanarProjection(I, pxDim, [1,0,0], func) 
    displayImage(xP, '', xH, xV)
    