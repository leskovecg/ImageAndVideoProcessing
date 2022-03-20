import numpy as np 
from labvaja6.vaja06 import getParameters 
from labvaja9.vaja09 import transformImage
from labvaja1.vaja01 import loadImage

def exhaustiveRegistration (iImageA, iImageB, iTx, iTy):
 
    X = np.arange(iTx[0], iTx[1]+1, iTx[2])
    Y = np.arange(iTy[0], iTy[1]+1, iTy[2])
    oMap = np.zeros([len(Y), len(X)])
    oTx = []
    oTy = []
    oImage = np.array(iImageB)
    # I je št. stolpcev
    # J je št. vrstic
    
    I = iImageA.shape[1]
    J = iImageA.shape[0]

    [tx_min, tx_max, delta_tx] = iTx
    [ty_min, ty_max, delta_ty] = iTy
    
    for i in range(0, len(X), delta_tx):
        for j in range(0, len(Y), delta_ty):
            
            oT = getParameters("affine", scale=[1, 1], trans=[i, j], rot=0, shear=[0, 0])
            oImage = transformImage(iType = 'affine', iImage = oImage, iDim = [1,1], iP = oT, iBgr = 0, iInterp = 1)
            
            MP = (iImageA - oImage)**2 / (I*J)
            
            oMap[j,i] = MP
            
            oTx.append(i)
            oTy.append(j)

            
    return oMap, oTx, oTy

 

if __name__ == "__main__":
    imSize = [100, 83]  # x, y
    ref_slika = loadImage("labvaja9\data\head-T2-083x100-08bit.raw", imSize, np.uint8)
    vhodna_slika1 = loadImage("labvaja9\data\head-SD-083x100-08bit.raw", imSize, np.uint8)
    vhodna_slika2 = loadImage("labvaja9\data\head-T1-083x100-08bit.raw", imSize, np.uint8)
    
    exhaustiveRegistration(ref_slika, vhodna_slika1, [-15, 15, 1], [-10, 20, 1])
    exhaustiveRegistration(ref_slika, vhodna_slika2, [-15, 15, 1], [-10, 20, 1])

