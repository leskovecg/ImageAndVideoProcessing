import numpy as np
import matplotlib.pyplot as plt
from labvaja1.vaja01 import loadImage
from labvaja1.displayImage import displayImage

## 1. NALOGA
if __name__ == "__main__":
    imSize = [256, 512]  # x, y
    pxDim = [2, 1]  # dx, dy
    gX = np.arange(imSize[0]) * pxDim[0]
    gY = np.arange(imSize[1]) * pxDim[1]
    I = loadImage("labvaja6\data\lena-256x512-08bit.raw", imSize, np.uint8)
    displayImage(I, "Originalna slika", gX, gY)

## 2. NALOGA
def getRadialValue(iXY, iCP):
    """
    vec-vrsticni komentarji
    iXY = [x, y] nasa tocka
    iCP = [
        [x1, y1],
        [x2, y2],
        [x3, y3],
        [x4, y4]
        ]
    """
    K = iCP.shape[0]
    # inicializacija vrednosti
    oValue = np.zeros(K)

    # i-ta tocka
    x_i = iXY[0]
    y_i = iXY[1]

    for k in range(K):
        # k-ta tocka
        x_k = iCP[k, 0]
        y_k = iCP[k, 1]
        # razadalja med naso tocko in k-to kontrolno tocko
        r = np.sqrt((x_i - x_k) ** 2 + (y_i - y_k) ** 2)
        # vrednost radialne funkcije
        if r > 0:
            oValue[k] = -(r ** 2) * np.log(r)
    return oValue


def getParameters(iType, **kwargs):
    if iType == "affine":
        # skaliranje
        Tk = np.array(
            [[kwargs["scale"][0], 0, 0], [0, kwargs["scale"][1], 0], [0, 0, 1]]
        )
        # translacija
        Tt = np.array(
            [[1, 0, kwargs["trans"][0]], [0, 1, kwargs["trans"][1]], [0, 0, 1]]
        )
        # rotacija
        phi = kwargs["rot"] * np.pi / 180  # pretvorba v radiane
        Tr = np.array(
            [[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi), 0], [0, 0, 1]]
        )
        # strig
        Tg = np.array(
            [[1, kwargs["shear"][0], 0], [kwargs["shear"][1], 1, 0], [0, 0, 1]]
        )
        # matrika afine preslikave
        oP = Tg @ Tr @ Tt @ Tk

    elif iType == "radial":
        # stevilo tock
        K = kwargs["orig_pts"].shape[0]

        # inicializacija matrike U
        U = np.zeros((K, K))

        coef_matrix = np.zeros((K, 2), dtype=float)

        # zanka cez vse i-je
        for i in range(K):
            U[i, :] = getRadialValue(kwargs["orig_pts"][i, :], kwargs["orig_pts"])

        # inverz matrike U
        U_inv = np.linalg.inv(U)
        # matricno resevanje linearnih enacb
        alphas = U_inv @ kwargs["mapped_pts"][:, 0]
        betas = U_inv @ kwargs["mapped_pts"][:, 1]

        # alfe in bete zapakiramo v stolpce ene same matrike
        coef_matrix[:, 0] = alphas
        coef_matrix[:, 1] = betas

        # izhodni slovar
        oP = {}
        oP["orig_pts"] = kwargs["orig_pts"]
        oP["coef"] = coef_matrix
    return oP


if __name__ == "__main__":
    # izracun transformacije matrike za afino transformacijo
    T_affine = getParameters("affine", scale=[1, 1], trans=[0, 0], rot=30, shear=[0, 0])

    # izracun parametrov za radialno transformacijo
    orig_pts = np.array([[0, 0], [511, 0], [0, 511], [511, 511]])
    mapped_pts = np.array([[0, 0], [511, 0], [0, 511], [255, 255]])
    oP = getParameters("radial", orig_pts=orig_pts, mapped_pts=mapped_pts)


## 3. NALOGA
def transformImage(iType, iImage, iDim, iP, iBgr=0, iInterp=0):

    # velikost vhodne slike
    [Y, X] = iImage.shape

    # inicializacija izhodne slike: vse vrednosti enake iBgr
    oImage = np.ones((Y, X)) * iBgr

    for y in range(Y):
        for x in range(X):
            # indeks piksla -> tocka v koor. sistemu
            pt = np.array([x, y]) * iDim

            # preslikava z afino transformacijo
            if iType == "affine":
                # iP je velikosti 3x3, zato pt dodamo enko
                pt = iP @ np.append(pt, 1)
                # zanima nas samo prva dva elementa vektorja pt [u, v, 1]
                pt = pt[:2]
            # preslikava z radialno transformacijo
            elif iType == "radial":
                # izracun vektorja U
                U = getRadialValue(pt, iP["orig_pts"])
                # izracunamo u in v, tako da vektor U pomnozimo z alfami in betami
                pt = np.array([U @ iP["coef"][:, 0], U @ iP["coef"][:, 1]])

            # preslikana tocka -> indeks piksla
            px = pt / iDim
            # interpolacija nictega reda
            if iInterp == 0:
                # najblizji sosed
                px = np.round(px).astype(np.int64)

                # filtriramo tocke: uporabimo samo tiste, ki so znotraj slike
                if px[0] >= 0 and px[0] < X and px[1] >= 0 and px[1] < Y:
                    oImage[y, x] = iImage[px[1], px[0]]
    return oImage


if __name__ == "__main__":
    # vrednost ozadja
    bgr = 63
    # potrebno je narediti inverzno preslikavo, ker transformImage omogoca le normalno interpolacijo (glej prosojnice)
    # afina preslikava
    tI = transformImage("affine", I, pxDim, iP=np.linalg.inv(T_affine), iBgr=bgr)
    displayImage(tI, "Afina", gX, gY)
    # radialna preslikava
    rI = transformImage("radial", I, pxDim, iP=oP, iBgr=bgr)
    displayImage(rI, "Radialna", gX, gY)
