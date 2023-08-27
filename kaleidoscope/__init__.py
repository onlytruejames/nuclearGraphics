from PIL import Image, ImageOps
import numpy as np
import math as maths
from random import choice, randint

lastImg = Image.new("RGB", (200, 200))

def resize(img, lastImg):
    r = min(img.width, img.height) / 2
    size = 2 * maths.sqrt((r**2) / 2)
    width, height = lastImg.size
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2
    lastImg = lastImg.crop((left, top, right, bottom))
    
    winWidth, winHeight = img.size
    width, height = size, size
    if winWidth / width < winHeight / height:
        resize = winHeight / height
    else:
        resize = winWidth / width
    lastImg = lastImg.resize((
        int(width * resize),
        int(height * resize)
    ))
    width, height = lastImg.size
    w, h = img.size
    left = (width - w) / 2
    top = (height - h) / 2
    right = (width + w) / 2
    bottom = (height + h) / 2
    return lastImg.crop((left, top, right, bottom))

def variables(dims, clb):
    global lastImg
    lastImg = Image.new("RGB", dims)

def callback(image):
    global lastImg
    image = image.convert("RGB")
    flip = ImageOps.flip(image)
    mirror = ImageOps.mirror(image)
    both = ImageOps.flip(mirror)
    img = Image.blend(Image.blend(image, flip, 0.5), Image.blend(mirror, both, 0.5), 0.5)
    lastImg = resize(img, lastImg).resize(img.size)
    img = Image.blend(img, lastImg, 0.5)
    lastImg = img.rotate(randint(0, 360), fillcolor=(0, 0, 0, 0))
    return img