from PIL import Image, ImageOps
import numpy as np
import math as maths
from random import choice, randint

global lastImg
lastImg = np.asarray(Image.new("RGB", (200, 200)))

def variables(cam):
    global lastImg
    lastImg = np.asarray(Image.new("RGB", (cam.get(3), cam.get(4))))
    return []

def callback(image, variables):
    global lastImg
    img = choice([np.maximum, np.minimum])(image, lastImg)
    img = Image.fromarray(img)
    lastImg = img
    return img