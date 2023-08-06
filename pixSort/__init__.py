from PIL import Image, ImageOps
import numpy as np
import math as maths
from random import choice, randint
import noise

global lastImg, frame
lastImg = Image.new("RGB", (200, 200))
frame = 0

map = [noise.pnoise2(maths.cos(maths.pi / (x * 100 + 0.1)), maths.sin(maths.pi / (x * 100 + 0.1))) for x in range(256)]

def sorts(img):
    global frame
    for line in range(0, len(img), 1):
        img[line] = np.array(sorted(list(img[line]), key = lambda x: map[int(
            (int(x[0]) + 
            int(x[1]) + 
            int(x[2])) / 3 + frame * 3
        ) % 255]))
    return img

def variables(dims, clb):
    global lastImg
    lastImg = Image.new("RGB", dims)
    return []

def changeDims(dims):
    global lastImg
    lastImg = lastImg.resize(dims)

def callback(image, variables):
    global lastImg, frame
    image = Image.blend(image, lastImg, 0.5)
    match frame % 4:
        case 1:
            image = image.transpose(Image.ROTATE_90)
        case 2:
            image = image.transpose(Image.ROTATE_180)
        case 3:
            image = image.transpose(Image.ROTATE_270)
    img = sorts(np.array(image),)
    img = Image.fromarray(img)
    match frame % 4:
        case 1:
            img = img.transpose(Image.ROTATE_270)
        case 2:
            img = img.transpose(Image.ROTATE_180)
        case 3:
            img = img.transpose(Image.ROTATE_90)
    lastImg = img
    frame += 1
    return img