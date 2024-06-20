from PIL import Image
import numpy as np

global lastImg, dims

def variables(dim, clb):
    global dims, lastImg
    dims = dim
    lastImg = False

def changeDims(dim):
    global dims, lastImg
    dims = dim
    if not type(lastImg) == bool:
        lastImg = np.array(Image.fromarray(lastImg.astype(np.uint8)).resize(dims)).astype(np.int16)

def callback(img):
    global dims, lastImg
    img = np.array(img).astype(np.int16)
    if type(lastImg) == bool:
        lastImg = img
    img = (lastImg + np.clip(img - lastImg, -5, 5)).astype(np.uint8)
    lastImg = img.astype(np.int16)
    return Image.fromarray(img)