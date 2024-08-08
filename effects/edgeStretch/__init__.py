from PIL import Image
import numpy as np
from random import randint, choice

getDecay = lambda: int((randint(20, 40) / 10) ** 2)
getDir = lambda: int((randint(10, 25) / 10) ** 2) * choice([-1, 1])

def variables(dims, clb):
    global lastImg, baseImg, direction, decay
    lastImg = Image.new("RGBA", dims, (0, 0, 0, 0))
    baseImg = Image.new("RGBA", dims, (0, 0, 0, 0))
    direction = (getDir(), getDir())
    decay = getDecay()

def changeDims(dims):
    global lastImg, baseImg
    lastImg = lastImg.resize(dims)
    baseImg = Image.new("RGBA", dims, (0, 0, 0, 0))

def callback(img):
    global lastImg, direction, decay
    decay -= 1
    if decay <= 0:
        direction = (getDir(), getDir())
        decay = getDecay()
    lastImg = np.array(lastImg)
    lastImg = np.roll(lastImg, direction, (0, 1))
    lastImg = Image.fromarray(lastImg)
    lastImg = Image.alpha_composite(lastImg, img)
    return lastImg