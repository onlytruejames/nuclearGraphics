from PIL import Image
import numpy as np
from random import choice, randint

global lastImg
lastImg = np.asarray(Image.new("RGB", (200, 200)))

def addtract(img, lastImg):
    lastImg -= 127
    img = np.add(img, lastImg)
    return img

def subadd(img, lastImg):
    lastImg += 127
    img = np.subtract(img, lastImg)
    return img

def invert1(img, lastImg):
    return np.floor_divide((255 - img) + (255 - lastImg), 2)

def invert2(img, lastImg):
    img = np.floor_divide(255 - img, 2)
    lastImg = np.floor_divide(lastImg, 4)
    lastImg = np.roll(lastImg, 1, axis=[1, 0, 0])
    img -= lastImg
    lastImg = np.roll(lastImg, 1, axis=[1, 0, 0])
    img -= lastImg
    return img

def rain2bow(img, lastImg):
    one = np.roll(lastImg, 1, axis=(1, 0))
    two = np.roll(lastImg, 1, axis=(0, 1))
    three = np.roll(lastImg, -1, axis=(1, 0))
    four = np.roll(lastImg, -1, axis=(0, 1))
    img += np.floor_divide(one + two + three + four, 4)
    img += np.roll(img, 1, axis=(0, 0, 1))
    return img + np.roll(img, 2, axis=(0, 0, 1))

def difference(img, lastImg):
    img = img.sum(axis=2, dtype=np.uint8)
    lastImg = lastImg.sum(axis=2, dtype=np.uint8)
    one = np.roll(lastImg, 1, axis=(1, 0))
    two = np.roll(lastImg, 1, axis=(0, 1))
    three = np.roll(lastImg, -1, axis=(1, 0))
    four = np.roll(lastImg, -1, axis=(0, 1))
    img += np.floor_divide(one + two + three + four, 4)
    img = Image.fromarray(img)
    return np.asarray(img.convert("RGB"))

effects = [addtract, subadd, invert1, invert2, rain2bow, difference]

def variables(cam, clb):
    global lastImg
    lastImg = np.asarray(Image.new("RGB", (int(cam.get(3)), int(cam.get(4)))))
    return [lastImg]

def callback(image, variables):
    global lastImg
    img = choice(effects)(np.asarray(image), lastImg)
    lastImg = img
    return Image.fromarray(img)