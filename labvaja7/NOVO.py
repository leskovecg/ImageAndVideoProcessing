import numpy as np
import matplotlib.pyplot as plt
from labvaja1.vaja01 import loadImage
from labvaja1.displayImage import displayImage
from labvaja7.vaja07 import spatialFiltering

## 1. NALOGA:
if __name__ == "__main__":
    I = loadImage("labvaja7\data\cameraman-256x256-08bit.raw", [256, 256], np.uint8)
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
    
## 2.NALOGA:
def weightedAverageFilter(iM, iN, iValue=2):
 
    a = np.linspace(-(iN - 1) / 2, (iM - 1) / 2, iN)
    b = iValue**(-np.abs(a))*(iN-1)
    oFilter = np.outer(b, b)
    
    return oFilter

weightedAverageFilter(3,3)
weightedAverageFilter(5,5)


## 3.NALOGA:
if __name__ == "__main__":
    
    K1 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kI1 = spatialFiltering("kernel", iImage=I, iFilter=K1)
    displayImage(kI1, "Sobelov operator za x smer")
    
    
    K2 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    kI2 = spatialFiltering("kernel", iImage=I, iFilter=K2)
    displayImage(kI2, "Sobelov operator za y smer")
    
    
    kIam = np.sqrt(kI1**2 + kI2**2)
    displayImage(kIam, "Amplitudni odziv")
    
    
    kIfaza = np.arctan(kI2/kI1)
    displayImage(kIfaza, "Fazni odziv")
    
    
    
## 4.NALOGA:
if __name__ == "__main__":
    I = loadImage("labvaja7\data\cameraman-256x256-08bit.raw", [256, 256], np.uint8)
    displayImage(I, "original")
    
    K = np.array([[0.01, 0.08, 0.01], [0.08, 0.64, 0.08], [0.01, 0.08, 0.01]])
    kI = spatialFiltering("kernel", iImage=I, iFilter=K)
    displayImage(kI, "zglajena z gaussom")
    
    m = I - kI
    displayImage(m, "maska")
    
    g = I + 2*m
    displayImage(g, "izostreno")

## 5.NALOGA:

## 6.NALOGA:

