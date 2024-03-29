from PIL import Image
from random import randint
import numpy as np

global rOffset, gOffset, bOffset
rOffset = (5, 0)
gOffset = (0, 5)
bOffset = (0, 0)

def variables(dims, clb):
    width, height = dims
    global rOffset, gOffset, bOffset
    rOffset = (5, 0)
    gOffset = (0, 5)
    bOffset = (0, 0)

def callback(image):
    global rOffset, gOffset, bOffset
    image = image.split()
    r = Image.fromarray(np.roll(np.array(image[0]), rOffset, axis=(0, 1)))
    g = Image.fromarray(np.roll(np.array(image[1]), gOffset, axis=(0, 1)))
    b = Image.fromarray(np.roll(np.array(image[2]), bOffset, axis=(0, 1)))
    image = Image.merge("RGB", (r, g, b))
    rOffset = (
        rOffset[0] + randint(-1, 1),
        rOffset[1] + randint(-1, 1)
    )
    gOffset = (
        gOffset[0] + randint(-1, 1),
        gOffset[1] + randint(-1, 1)
    )
    bOffset = (
        bOffset[0] + randint(-1, 1),
        bOffset[1] + randint(-1, 1)
    )
    return image