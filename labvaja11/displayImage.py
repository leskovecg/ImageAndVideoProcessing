from matplotlib import pyplot as plt 


def displayImage (iImage, iTitle, iGridX=None, iGridY=None, show = True):
    # ustvarimo prikazno okno
    fig = plt.figure()
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
    if show == True:
        plt.show()

    return fig