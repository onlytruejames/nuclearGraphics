from PIL import Image, ImageFilter
import numpy as np
import math as maths

gaussian = ImageFilter.GaussianBlur()

def variables(dims, clb):
    global x
    x = 0

def callback(img):
    global x
    x += 0.1
    if x > maths.pi * 2:
        x = 0
    if x < 0:
        x = maths.pi * 2
    mask = np.array(img.filter(gaussian).convert("L")).astype("float64")
    mask1 = np.where(mask < maths.sin(x) * 255 + 255, True, False)
    mask2 = np.where(mask > maths.sin(x) * 255, True, False)
    mask = np.where(mask1 == mask2, 255, 0)
    img.putalpha(Image.fromarray(mask.astype("uint8")))
    return img