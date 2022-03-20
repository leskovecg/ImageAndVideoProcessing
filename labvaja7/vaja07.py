import numpy as np
import matplotlib.pyplot as plt
from labvaja1.vaja01 import loadImage
from labvaja1.displayImage import displayImage

## 1. NALOGA:
if __name__ == "__main__":
    I = loadImage("labvaja7\data\cameraman-256x256-08bit.raw", [256, 256], np.uint8)
    displayImage(I, "Originalna slika")


## 2. NALOGA:
def spatialFiltering(iType, iImage, iFilter, iStatFunc=None, iMorphOp=None):
    # podatki o filtru
    N, M = iFilter.shape
    n = np.floor((N - 1) / 2).astype(int)
    m = np.floor((M - 1) / 2).astype(int)

    # razsiritev prostorske domene
    iImage = changeSpatialDomain("enlarge", iImage=iImage, iX=m, iY=n)

    Y, X = iImage.shape
    oImage = np.zeros((Y, X), dtype=float)

    # filtriranje slike
    for y in range(n, Y - n):
        for x in range(m, X - m):
            # delcek slike, ki pripada filtru
            patch = iImage[y - n : y + n + 1, x - m : x + m + 1]

            # filtriranje z jedrom
            if iType == "kernel":
                s = (patch * iFilter).sum()
                oImage[y, x] = s
            # statisticno filtriranje
            elif iType == "statistical":
                oImage[y, x] = iStatFunc(patch)
            # morfološko filtriranje
            elif iType == "morphological":
                R = patch[iFilter != 0]  # dobimo vektor stevil
                if iMorphOp == "erosion":
                    oImage[y, x] = R.min()
                elif iMorphOp == "dilation":
                    oImage[y, x] = R.max()
                else:
                    NotImplementedError("neznan iMorphOp")
                    return None
            else:
                NotImplementedError(f"{iType} is not supported")
                return None

    # zmanjsanje prostorske domene izhodne slike
    oImage = changeSpatialDomain("reduce", iImage=oImage, iX=m, iY=n)

    return oImage


# 3. NALOGA:
def changeSpatialDomain(iType, iImage, iX, iY, iMode=None, iBgr=0):
    # velikost slike
    Y, X = iImage.shape

    # razsiritev prostorske domene
    if iType == "enlarge":
        if iMode is None:
            oImage = np.zeros((Y + 2 * iY, X + 2 * iX))
            oImage[iY : iY + Y, iX : iX + X] = iImage
        # elif iMode == ...

    elif iType == "reduce":
        oImage = iImage[iY : Y - iY, iX : X - iX]
    return oImage


## 2. NALOGA:
if __name__ == "__main__":
    # filtriranje z jedrom
    K = 1 / 16 * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    kI = spatialFiltering("kernel", iImage=I, iFilter=K)
    displayImage(kI, "Filtrirana slika - filtriranje z jedrom")

    # statisticno filtriranje
    sI = spatialFiltering(
        "statistical", I, iFilter=np.zeros((3, 3)), iStatFunc=np.median
    )
    displayImage(sI, "Filtrirana slika - statisticno filtriranje")

    # morfolosko filtriranje
    SE = np.array(
        [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
        ]
    )
    mI = spatialFiltering("morphological", I, iFilter=SE, iMorphOp="erosion")
    displayImage(mI, "Filtrirana slika - morfolosko filtriranje")


if __name__ == "__main__":
    changeSpatialDomain("enlarge", np.ones((5, 5)), iX=3, iY=2)
    
