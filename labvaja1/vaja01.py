from matplotlib import pyplot as plt 
import numpy as np 

## 1. naloga:
if __name__ == '__main__':
    im = plt.imread('labvaja1\data\lena-color.png')

    # vrne nam obliko in velikost
    print(im.shape)
    print(im.size)

    # ustvarimo prikazno okno 
    plt.figure()
    plt.imshow(im)
    plt.imsave('labvaja1\data\LENA-color.jpeg', im) # sliko dobiš


## 2. naloga:
def loadImage (iPath, iSize, iType):

    # odpremo datoteko v načinu za branje 
    fid = open(iPath, 'rb')
    buffer = fid.read()

    buffer_len = len(np.frombuffer(buffer=buffer, dtype=iType))

    if buffer_len == np.prod(iSize):
        oImage_shape = [iSize[1], iSize[0]]
    else:
        oImage_shape = [iSize[1], iSize[0], 3]
    oImage = np.ndarray(oImage_shape, iType, buffer, order='F')

    
    fid.close()
    
    return oImage 

if __name__ == '__main__':
    # naložimo sivinsko sliko
    i_gray = loadImage('labvaja1\data\lena-gray-410x512-08bit.raw', [410,512], np.uint8)
    plt.figure()
    plt.imshow(i_gray, cmap=plt.cm.gray)

    # naložimo barvno sliko
    i_color = loadImage('labvaja1\data\lena-color-512x410-08bit.raw', [512,410], np.uint8)
    plt.figure()
    plt.imshow(i_color, cmap=plt.cm.gray)


## 3. naloga:
def displayImage(iImage ,iTitle=''):

    plt.figure()
    plt.title(iTitle)

    plt.imshow(iImage, cmap=plt.cm.gray, vmin=0, vmax=255, aspect='equal')

    plt.show()

if __name__ == '__main__':
    displayImage(i_gray, 'Sivinska slika:')
    displayImage(i_color, 'Barvna slika:')
    
    
## DODATEK:
def saveImage(iImage, iPath, iType):
    with open(iPath, 'wb') as file:
        file.write(np.ascontiguousarray(iImage.astype(iType)))
        
if __name__ == '__main__':
    saveImage(i_gray, "labvaja1\data\moja_slika.raw", np.uint8)


