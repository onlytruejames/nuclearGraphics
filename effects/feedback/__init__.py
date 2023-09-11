from PIL import Image, ImageFilter
import numpy as np
import random

gaussian = ImageFilter.GaussianBlur(radius=1)

def variables(dims, clb):
    global lastImg, location, rotation, expansion, locVel, rotVel, expVel, baseImg
    baseImg = Image.new("RGBA", dims, (0, 0, 0, 0))
    lastImg = Image.new("RGBA", dims)
    location = np.array([0, 0], dtype=np.float64)
    rotation = 0
    expansion = 1
    locVel = np.array([0, 0], dtype=np.float64)
    rotVel = 0
    expVel = 0

def changeDims(dims):
    global lastImg, baseImg
    lastImg = lastImg.resize(dims)
    baseImg = baseImg.resize(dims)

def callback(img):
    img = img.convert("RGBA")
    global lastImg, location, rotation, expansion, locVel, rotVel, expVel, baseImg
    lastImg = lastImg.filter(gaussian)
    location += locVel
    rotation += rotVel
    expansion += expVel
    location = np.clip(location, -min(img.width, img.height) / 2, min(img.width, img.height) / 2)
    locVel = np.clip(locVel, -5, 5)
    rotVel += random.randint(-5, 5) / 10
    rotation = rotation % 360
    if expansion < 0.3:
        expansion = 0.3
        expVel = 0
    if expansion > 1.5:
        expansion = 1.5
        expVel = 0
    if not 20 > rotVel > -20:
        rotVel = 0
    locVel += np.array([random.randint(-2, 2) / 10, random.randint(-2, 2) / 10], dtype=np.float64)
    rotVel += random.randint(-2, 2)
    expVel += random.randint(-2, 2) / 10
    lastImg = lastImg.resize(tuple((np.array(lastImg.size) * expansion).astype(np.int64)))
    lastImg = lastImg.rotate(rotation, expand=True, fillcolor=(0, 0, 0, 0))
    loc = tuple((location + np.array(img.size) / 2 - np.array(lastImg.size) / 2).astype(np.int64))
    base = baseImg.copy()
    base.paste(lastImg, loc)
    img = Image.alpha_composite(img, base)
    lastImg = img
    return img