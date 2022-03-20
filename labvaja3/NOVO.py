import numpy as np
from matplotlib import pyplot as plt
from labvaja1.vaja01 import displayImage, loadImage
from labvaja2.vaja02 import computeHistogram, displayHistogram
from labvaja3.vaja03 import interpolateImage

## 1. NALOGA:
if __name__ == '__main__':
    I = loadImage('labvaja3\data\pumpkin-200x152-08bit.raw', [200,152], np.uint8)
    displayImage(I,'originalna slika')
    
Islika = np.zeros([50, 65])
for x in range(0,65,1):
    for y in range(0,50,1):
        s = 0
        tocka = np.array([x, y])
        s = I[tocka[1] + 30, tocka[0] + 75]
        Islika[y,x] = s
Islika = Islika.astype(int)
displayImage(Islika,'Interpolacijska slika 65 X 50:')


histogram, _, _, levels = computeHistogram(Islika)
displayHistogram(histogram, levels, 'Histogram interpolacijske slike:')

# minimalna sivinska vrednost:
print(Islika.min())

# maksimalna sivinska vrednost:
print(Islika.max())

# povprečna vrednost:
print(int(np.round(np.average(Islika))))


## 2. in 3. NALOGA:
if __name__ == '__main__':
    intSize = [600, 300]
    # rob je stopničast
    I0 = interpolateImage(I, intSize, 0)
    I0 = I0.astype(int)
    displayImage(I0, 'Interpolirana slika pri 600 X 300 (red 0):')

    # rob je zglajen
    I1 = interpolateImage(I, intSize, 1)
    I1 = I1.astype(int)
    displayImage(I1, 'Interpolirana slika pri 600 X 300 (red 1):')


histogram, _, _, levels = computeHistogram(I0)
displayHistogram(histogram, levels, 'Histogram interpolirane slike (red 0):')

# minimalna sivinska vrednost:
print(I0.min())

# maksimalna sivinska vrednost:
print(I0.max())

# povprečna vrednost:
print(int(np.round(np.average(I0))))

   
histogram, _, _, levels = computeHistogram(I1)
displayHistogram(histogram, levels, 'Histogram interpolirane slike (red 1):')

# minimalna sivinska vrednost:
print(I1.min())

# maksimalna sivinska vrednost:
print(I1.max())

# povprečna vrednost:
print(int(np.round(np.average(I1))))

## 4. NALOGA:


## 5. NALOGA:
def displayImage(iImage, iTitle, iGridX=None, iGridY=None):
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
