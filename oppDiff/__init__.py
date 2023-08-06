from PIL import Image, ImageOps
import numpy as np
import math as maths
from random import choice, randint

global lastImg
lastImg = np.array(Image.new("RGB", (200, 200)))

def variables(dims, clb):
    global lastImg
    lastImg = np.array(Image.new("RGB", dims))
    return []

def changeDims(dims):
    global lastImg
    lastImg = np.array(Image.fromarray(lastImg).resize(dims))

def callback(image, variables):
    global lastImg
    image = np.array(image)
    img = lastImg + (lastImg - image)
    lastImg = image
    img = Image.fromarray(img)
    return img