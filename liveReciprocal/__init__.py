from PIL import Image
import numpy as np
from random import choice, randint

global lastImg
lastImg = np.asarray(Image.new("RGB", (200, 200)))

def reciprocal(img, lastImg):
    img = (1 / ((img + lastImg) / 2 + 0.1) * randint(100, 500)).astype(np.uint8)
    return np.roll(img, randint(0, 2), axis=2)

def variables(cam):
    global lastImg
    lastImg = np.asarray(Image.new("RGB", (int(cam.get(3)), int(cam.get(4)))))
    return [lastImg]

def callback(image, variables):
    global lastImg
    img = reciprocal(image, lastImg)
    lastImg = img
    return Image.fromarray(img)