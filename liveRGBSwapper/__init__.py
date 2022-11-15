from random import shuffle, randint
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB
from math import sin, pi
from PIL import (
    Image,
    ImageTk
)
import tkinter

halfPi = pi / 2

def variables(cam):
    return []

def callback(cam, variables):
    result, image = cam.read()
    if result:
        image = list(image.split())
        shuffle(image)
        return Image.merge("RGB", tuple(image))

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