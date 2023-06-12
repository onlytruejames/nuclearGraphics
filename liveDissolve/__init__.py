from PIL import Image
import numpy as np
import math as maths
from random import choice, randint

global lastImg
lastImg = np.array(Image.new("RGB", (200, 200)))

def variables(cam, clb):
    global lastImg
    lastImg = np.array(Image.new("RGB", (cam.get(3), cam.get(4))))
    return []

def callback(image, variables):
    global lastImg
    img = image
    newLast = np.zeros(lastImg.shape, dtype="uint8")
    for d in [[10, 0], [0, 10], [-10, 0], [0, -10]]:
        newLast += np.floor_divide(np.roll(lastImg, (d[0], d[1]), axis=(0, 1)), 4)
    img = Image.blend(img, Image.fromarray(newLast), 0.8)
    
    lastImg = np.array(img)
    return img
