from PIL import Image, ImageOps
import numpy as np
import math as maths
from random import choice, randint

def variables(dims, clb):
    global lastImg
    lastImg = np.array(Image.new("RGB", dims))

def changeDims(dims):
    global lastImg
    lastImg = np.array(Image.fromarray(lastImg).resize(dims))

def callback(image):
    alpha = image.getchannel("A")
    image = image.convert("RGB")
    global lastImg
    image = np.array(image)
    img = lastImg + (lastImg - image)
    lastImg = image
    img = Image.fromarray(img)
    img.putalpha(alpha)
    return img