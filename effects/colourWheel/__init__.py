from math import sin, cos, pi
from PIL import Image
import numpy as np

global i
i = 0

def callback(image):
    global i
    r = np.array(image.getchannel("R")).astype(np.float64)
    g = np.array(image.getchannel("G")).astype(np.float64)
    b = np.array(image.getchannel("B")).astype(np.float64)
    if i < 1:
        one = [r, g, b]
        two = [g, b, r]
    elif i < 2:
        one = [g, b, r]
        two = [b, r, g]
    else:
        one = [b, r, g]
        two = [r, g, b]
    j = i % 1
    r = Image.fromarray((two[0] * j + one[0] * (1 - j)).astype(np.uint8), mode="L")
    g = Image.fromarray((two[1] * j + one[1] * (1 - j)).astype(np.uint8), mode="L")
    b = Image.fromarray((two[2] * j + one[2] * (1 - j)).astype(np.uint8), mode="L")
    rgb = (r, g, b, image.getchannel("A"))
    i += 0.1
    i = i % 3
    return Image.merge("RGBA", rgb)