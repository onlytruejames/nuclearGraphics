from PIL import Image
import numpy as np
import math as maths
from random import choice, randint

def variables(dims, clb):
    global lastImg
    lastImg = np.array(Image.new("RGBA", dims))

def changeDims(dims):
    global lastImg
    lastImg = np.array(Image.fromarray(lastImg).resize(dims))

def callback(image):
    global lastImg
    img = image
    newLast = np.zeros(lastImg.shape, dtype="uint8")
    for d in [[10, 0], [0, 10], [-10, 0], [0, -10]]:
        newLast += np.floor_divide(np.roll(lastImg, (d[0], d[1]), axis=(0, 1)), 4)
    img = Image.blend(img, Image.fromarray(newLast), 0.8)
    lastImg = np.array(img)
    return img
