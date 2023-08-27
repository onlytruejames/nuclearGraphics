from PIL import Image
import numpy as np
from math import sin

def variables(dims, clb):
    global i
    i = 0

def callback(img):
    global i
    i += 0.1
    if i > 3.1:
        i = 0
    img = np.array(img).astype(np.float64)
    img = (np.sin(img / 10) + sin(i) * 5 + 10) * 127.5
    return Image.fromarray(img.astype(np.uint8))