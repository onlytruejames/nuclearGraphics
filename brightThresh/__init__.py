from PIL import Image, ImageFilter
import numpy as np
import random
import math as maths

gaussian = ImageFilter.GaussianBlur()

def variables(dims, clb):
    global x
    x = 0
    return []

def callback(img, variables):
    global x
    x += 0.1
    if x > maths.pi:
        x = 0
    if x < 0:
        x = maths.pi
    mask = np.array(img.filter(gaussian).convert("L")).astype("float64")
    img = np.array(img)
    mask -= maths.sin(x) * (np.max(mask) - np.min(mask))
    mask = np.clip(np.floor(np.abs(mask)) - 10, 0, 1)
    return Image.fromarray(img * np.expand_dims(mask.astype("uint8"), 2))