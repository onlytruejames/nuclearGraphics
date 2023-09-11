from random import shuffle
from math import sin, pi
from PIL import (
    Image,
    ImageTk
)
import tkinter

halfPi = pi / 2

def callback(image):
    image = list(image.split())
    rgb = image[0:3]
    shuffle(rgb)
    rgb.append(image[3])
    return Image.merge("RGBA", tuple(rgb))

size = 99

def calc(x):
    x = x % size
    r = 0
    g = 0
    b = 0
    if x < size / 3:
        r = (sin((x / (size / 3 / pi * 2)) + halfPi))
        g = (sin(x / (size / 3 / pi * 2)))
    elif x < size / 3 * 2:
        g = (sin(((x - size / 3) / (size / 3 / pi * 2)) + halfPi))
        b = (sin((x - size / 3) / (size / 3 / pi * 2)))
    else:
        b = (sin(((x - size / 3 * 2) / (size / 3 / pi * 2)) + halfPi))
        r = (sin((x - size / 3 * 2) / (size / 3 / pi * 2)))
    return (r, g, b)

colours = [calc(x) for x in range(99)]