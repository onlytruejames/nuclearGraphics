from PIL import Image
import numpy as np
from random import choice, randint

global lastImg
lastImg = np.asarray(Image.new("RGB", (200, 200)))

def reciprocal(img, lastImg):
    img = (1 / ((img + lastImg) / 2 + 0.1) * randint(100, 500)).astype(np.uint8)
    return np.roll(img, randint(0, 2), axis=2)

def variables(dims, clb):
    global lastImg
    lastImg = np.array(Image.new("RGB", dims))

def changeDims(dims):
    global lastImg
    lastImg = np.array(Image.fromarray(lastImg).resize(dims))

def callback(image):
    global lastImg
    img = reciprocal(image, lastImg)
    lastImg = img
    return Image.fromarray(img)