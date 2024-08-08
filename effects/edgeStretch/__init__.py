from PIL import Image
import numpy as np
from random import randint, choice, shuffle

getDecay = lambda: int((randint(20, 40) / 10) ** 2)
def getDir():
    dir = [int((randint(17, 25) / 17) ** 2) * choice([-1, 1]), int((randint(0, 25) / 17) ** 2) * choice([-1, 1])]
    shuffle(dir)
    return tuple(dir)

def variables(dims, clb):
    global lastImg, baseImg, direction, decay
    lastImg = Image.new("RGBA", dims, (0, 0, 0, 0))
    baseImg = Image.new("RGBA", dims, (0, 0, 0, 0))
    direction = getDir()
    decay = getDecay()

def changeDims(dims):
    global lastImg, baseImg
    lastImg = lastImg.resize(dims)
    baseImg = Image.new("RGBA", dims, (0, 0, 0, 0))

def callback(img):
    global lastImg, direction, decay
    decay -= 1
    if decay <= 0:
        direction = getDir()
        decay = getDecay()
    lastImg = np.array(lastImg)
    lastImg = np.roll(lastImg, direction, (0, 1))
    lastImg = lastImg.astype(np.int16) - 5
    lastImg = np.clip(lastImg, 0, 255).astype(np.uint8)
    lastImg = Image.fromarray(lastImg)
    lastImg = Image.alpha_composite(lastImg, img)
    return lastImg
