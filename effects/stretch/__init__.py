from PIL import Image, ImageStat
import numpy as np
import math as maths
from random import choice, randint

def variables(dims, clb):
    global lastImg
    lastImg = Image.new("RGB", dims)

def getAverageRGBN(image):
  im = np.array(image)
  w,h,d = im.shape
  im.shape = (w*h, d)
  return tuple(np.average(im, axis=0))

def callback(img):
    global lastImg
    brightness = abs(maths.cos(ImageStat.Stat(lastImg.convert("L")).mean[0] + randint(-2, 2))) * 255
    if maths.sin(brightness) >= 0:
        img = img.transpose(Image.ROTATE_90)
    img = np.array(img)
    width = int((brightness / 255) * (len(img) / 2))
    for line in range(len(img)):
        img[line][0:width] = img[line][width]
        img[line][-width:-1] = img[line][-width]
    img = Image.fromarray(img)
    if maths.sin(brightness) >= 0:
        img = img.transpose(Image.ROTATE_270)
    lastImg = img
    return img
