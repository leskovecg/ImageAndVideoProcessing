import cv2
from labvaja11.vaja11 import loadFrame
from labvaja11.displayImage import displayImage
from labvaja11.vaja11 import displayMotionField
from labvaja11.vaja11 import blockMatching
    
# 1: NALOGA:

# 2: NALOGA:
from PIL import Image
import io

frames = []

V1 = cv2.VideoCapture("labvaja11/data/simple-video.avi")
bsize = [8, 8]
searchSize = 15
    
def fig2img(fig):
    """ 
    Convert a Matplotlib figure to a PIL Image and return it 
    """
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    
    return img

for i in range(0, 153):
    I1 = loadFrame(V1, iK = i)
    I2 = loadFrame(V1, iK = i + 1)
    
    MF, CP = blockMatching(I1, I2, bsize, searchSize)
    
    fig = displayMotionField(MF, CP, iTitle='Superponirani vektorji premika', iImage = I1)
    img = fig2img(fig)
    frames.append(img)

# shranimo v GIF datoteko:
frames[0].save(
    "labvaja11/data/frames_gif.gif",
    duration = 40, 
    loop = 0,
    save_all = True,
    optimize = False,
    append_images = frames[1:],
    disposal = 3
)



# 3: NALOGA:
if __name__ == '__main__':
    
    V1 = cv2.VideoCapture("labvaja11/data/real-video.avi")
    
    print(f'število slik v videu: {int(V1.get(cv2.CAP_PROP_FRAME_COUNT))}')
    I1 = loadFrame(V1, iK = 70)
    I2 = loadFrame(V1, iK = 71)
    
    displayImage(I1, 'slika 1')
    displayImage(I2, 'slika 2')
    
    bsize = [8, 8]
    searchSize = 15
    MF, CP = blockMatching(I1, I2, bsize, searchSize)
    
    displayMotionField(MF, CP, iTitle='Vektorji premika')
    displayMotionField(MF, CP, iTitle='Superponirani vektorji premika', iImage = I1)
