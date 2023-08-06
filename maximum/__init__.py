from PIL import Image, ImageOps
import numpy as np
import math as maths
from random import choice, randint

global lastImg

def variables(dims, clb):
    global lastImg
    lastImg = Image.new("RGB", dims)
    return []

def changeDims(dims):
    global lastImg
    lastImg = lastImg.resize(dims)

def callback(image, variables):
    global lastImg
    img = choice([np.maximum, np.minimum])(image, lastImg)
    img = Image.fromarray(img)
    lastImg = img
    return img