import numpy as np 
from matplotlib import pyplot as plt
from labvaja1.vaja01 import loadImage, displayImage

## 1. NALOGA:
if __name__ == '__main__':
    # naložimo sliko iz mape labvaja2/data
    I = loadImage('labvaja2/data/valley-1024x683-08bit.raw', (1024,683), np.uint8)
    # prikažemo sliko s funkcijo, ki smo jo napisali zadnjič
    displayImage(I,'originalna slika')


## 2. NALOGA:
def computeHistogram(iImage):
    # območje intezitet slik 0, ...., Lmax
    n_bits = int(np.floor(np.log2(iImage.max())) + 1)
    
    oLevels = np.arange(0, 2**n_bits, 1)

    oHist = np.zeros_like(oLevels)
    for y in range(iImage.shape[0]): # for gre po y-osi od 0 do image heighta 
        for x in range(iImage.shape[1]): # for gre po x-osi od 0 do image widtha
            oHist[iImage[y, x]] = oHist[iImage[y, x]] + 1


    oProb = oHist / iImage.size

    # kumulativna porazdelitev
    oCDF = np.zeros_like(oProb)
    for i in range(len(oProb)):
        oCDF[i] = oProb[0:i].sum()

    return oHist, oProb, oCDF, oLevels


def displayHistogram(iHist, iLevels, iTitle):
    plt.figure()

    plt.title(iTitle)

    plt.bar(iLevels, iHist, width=1, edgecolor='darkred', color='red')

    # nastavimo x in y os, tako da se vse vidi
    plt.xlim(iLevels.min(), iLevels.max())
    plt.ylim(0, 1.05*iHist.max())

    plt.show()


if __name__ == '__main__':
    histogram, norm_histogram, kumalativna_porazd, levels = computeHistogram(I)

    displayHistogram(histogram, levels, 'Histogram:')
    displayHistogram(norm_histogram, levels, 'Normalizirani histogram:')
    displayHistogram(kumalativna_porazd, levels, 'Kumulativna porazdelitev verjetnosti:')


## 3. NALOGA:
def equalizeHistogram(iImage):
    # pomeni, da si te vrednosti ne shranimo v nobeno spremenljivko
    _, _, cdf, _ = computeHistogram(iImage)

    n_bits = int(np.floor(np.log2(iImage.max())) + 1)

    max_intensity = 2**n_bits - 1 # maksimalna sivinska vrednost==255

    oImage = np.zeros_like(iImage)
    for y in range(iImage.shape[0]):
        for x in range(iImage.shape[1]):
            vhodna_intenziteta = iImage[y, x]
            preslikana_intenziteta = np.floor(max_intensity*cdf[vhodna_intenziteta])
            oImage[y,x] = preslikana_intenziteta
    return oImage


if __name__ == '__main__':
    I_eq = equalizeHistogram(I)
    displayImage(I_eq,'Slika z izravnanim histogramom:') # poveča se kontrast

    hist, prob, cdf, levels = computeHistogram(I)
    hist1, prob1, cdf1, levels1 = computeHistogram(I_eq)

    displayHistogram(hist1, levels1, 'Histogram:')
    displayHistogram(prob1, levels1, 'Normalizirani histogram:')
    displayHistogram(cdf1, levels1, 'Kumulativna porazdelitev verjetnosti (CDF):')


## 4. NALOGA:
def computeEntropy(iImage):
    oEntropy = (-prob[prob>0]*(np.log2(prob[prob>0]))).sum()
    return oEntropy

if __name__ == '__main__':
    _, prob, _, _ = computeHistogram(I)
    entropija1 = computeEntropy(I)

    I_eq = equalizeHistogram(I)
    _, prob, _, _ = computeHistogram(I_eq)
    entropija2 = computeEntropy(I_eq)

    print("Entropija originalne slike: "+str(entropija1))
    print("Entropija slike z izravnanim histogramom: "+str(entropija2))
    
    
## DODATEK:
def addNoise(iImage, iStd):
    noise = iStd * np.random.randn(iImage.shape[0], iImage.shape[1])
    oImage = iImage + noise * 100
    return oImage, noise

if __name__ == '__main__':
    noisyI, noise = addNoise(I_eq, 1)
    displayImage(noisyI, "Šumna slika 1")
    
    noisyI, noise = addNoise(I_eq, 5)
    displayImage(noisyI, "Šumna slika 2")


    

    

