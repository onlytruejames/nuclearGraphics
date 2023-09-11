from PIL import Image, ImageEnhance
import numpy as np

def callback(img):
    return ImageEnhance.Color(img).enhance(2)