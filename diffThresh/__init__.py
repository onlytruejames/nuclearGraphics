from PIL import Image
import numpy as np

thresh = 50

def variables(dims, clb):
    global lastImg
    lastImg = False

def changeDims(dims):
    global lastImg
    if lastImg:
        lastImg = lastImg.resize(dims)

def callback(image):
    global lastImg
    if not lastImg:
        lastImg = image
    else:
        image = np.array(image).astype("int64")
        lastImg = np.array(lastImg).astype("int64")
        mask = np.clip(np.abs(lastImg - image) - thresh, 0, 1)
        image = Image.fromarray(((image * mask) + (lastImg * (1 - mask))).astype("uint8"))
        lastImg = image
    return image