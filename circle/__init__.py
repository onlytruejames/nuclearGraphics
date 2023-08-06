from PIL import Image
import numpy as np
import math as maths
from random import choice, randint
from skimage.draw import circle_perimeter

global lastImg, rings
rings = []
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
    global lastImg, rings
    width, height = dims
    centrey = int(width / 2 + 0.5)
    centrex = int(height / 2 + 0.5)
    for r1 in range(10, (int(min(width, height) / 2) - 10), 12):
        r = r1
        ones = np.ones((height, width, 3), dtype=np.uint8)
        for r2 in range(randint(r-10, r-2), randint(r+2, r+10), 1):
            rr, cc = circle_perimeter(centrex, centrey, r2)
            ones[rr, cc] = np.array([5, 5, 5], dtype=np.uint8)
        r = (int(min(width, height) / 2) - 10) - r1
        for r2 in range(randint(r-10, r-2), randint(r+2, r+10), 1):
            rr, cc = circle_perimeter(centrex, centrey, r2)
            ones[rr, cc] = np.array([0.8, 0.8, 0.8], dtype=np.uint8)
        rings.append(ones)
    lastImg = Image.new("RGB", (int(width), int(height)))
    return []

def changeDims(dims):
    global lastImg, rings
    lastImg = lastImg.resize(dims)
    newRings = []
    for ring in rings:
        newRings.append(np.array(Image.fromarray(ring).resize(dims)))
    rings = newRings

def callback(img, variables):
    global lastImg, rings
    img = (choice(rings) * np.array(img))
    img = img.astype(np.uint16)
    img = np.clip(img, 0, 255)
    img = img.astype(np.uint8)
    img = Image.fromarray(img)
    lastImg = resize(img, lastImg).resize(img.size)
    img = Image.blend(img, lastImg, 0.5)
    lastImg = img.rotate(randint(0, 360), fillcolor=(0, 0, 0, 0))
    return img