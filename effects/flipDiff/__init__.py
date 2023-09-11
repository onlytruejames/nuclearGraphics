from PIL import Image, ImageOps
import numpy as np
from random import choice, randint

global lastImg
lastImg = Image.new("RGB", (200, 200))

def difference(img, lastImg):
    img = img - lastImg
    img += 127
    img = Image.fromarray(img)
    return img.convert("RGB")

effects = [difference]

def variables(dims, clb):
    global lastImg
    lastImg = Image.new("RGB", dims)

def changeDims(dims):
    global lastImg
    lastImg = lastImg.resize(dims)

def callback(image):
    alpha = image.getchannel("A")
    image = image.convert("RGB")
    global lastImg
    img = choice(effects)(np.array(image), np.array(lastImg))
    lastImg = Image.blend(image, lastImg, 0.5)
    if randint(0, 1) == 0:
        lastImg = ImageOps.mirror(lastImg)
    else:
        lastImg = ImageOps.flip(lastImg)
    img.putalpha(alpha)
    return img