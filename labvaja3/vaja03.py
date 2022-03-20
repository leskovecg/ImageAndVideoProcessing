import numpy as np
from matplotlib import pyplot as plt
from labvaja1.vaja01 import loadImage, displayImage

## 1. NALOGA:
if __name__ == '__main__':
    I = loadImage('labvaja3\data\pumpkin-200x152-08bit.raw', [200,152], np.uint8)
    displayImage(I,'originalna slika')

## 2. NALOGA:
def interpolateImage(iImage, iSize, iOrder):
    iOrder = int(iOrder)

    # iImage - interpolacijska slika
    # oImage - interpolirana slika
    # iSize - vektor interpolirane slike

    oImage = np.zeros([iSize[1], iSize[0]])

    # korak interpolacije:  (dx, dy)
    step = [
        (iImage.shape[1]-1)/(iSize[0]-1),
        (iImage.shape[0]-1)/(iSize[1]-1)
    ]

    # interpolacija slike 
    for y in range(iSize[1]):
        for x in range(iSize[0]):
            s = 0 # s je inteziteta


            # točka v koordinatnem sistemu vhodne slike 
            pt = np.array([x, y])*np.array(step)

            if iOrder == 0:
                px = np.round(pt).astype(np.int64)
                s = iImage[px[1], px[0]]
            elif iOrder == 1:
                px = np.floor(pt).astype(np.int64)
                # oblika px: [xi, yi]
                
                a = abs((px[0]+1) - pt[0])*abs((px[1]+1) - pt[1]) # delimo z 1
                b = abs((px[0]+0) - pt[0])*abs((px[1]+1) - pt[1]) # delimo z 1
                c = abs((px[0]+1) - pt[0])*abs((px[1]+0) - pt[1]) # delimo z 1
                d = abs((px[0]+0) - pt[0])*abs((px[1]+0) - pt[1]) # delimo z 1

                # sa = sivinska vrednost povezana z a
                sa = iImage[px[1]+0, px[0]+0]
                sb = iImage[px[1]+0, min(px[0]+1, iImage.shape[1]-1)]
                sc = iImage[min(px[1]+1, iImage.shape[0]-1), px[0]+0]
                sd = iImage[min(px[1]+1, iImage.shape[0]-1), min(px[0]+1, iImage.shape[1]-1)]
                # z min funkcijo zagotovimo, da indeksi ne presežejo slike 

                s = np.floor(sa*a + sb*b + sc*c + sd*d) 

            oImage[y, x] = s
    return oImage

if __name__ == '__main__':
    intSize = [I.shape[1]*2, I.shape[0]*2]
    # rob je stopničast
    I0 = interpolateImage(I, intSize, 0)
    displayImage(I0, 'Interpolirana slika (red 0)')

    # rob je zglajen
    I1 = interpolateImage(I, intSize, 1)
    displayImage(I1, 'Interpolirana slika (red 1)')
