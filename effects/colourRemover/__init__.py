from PIL import Image, ImageFilter
import numpy as np
import random

gaussian = ImageFilter.GaussianBlur()

def callback(img):
    coords = (random.randint(0, img.width - 1), random.randint(0, img.height - 1))
    mask = np.array(img.filter(gaussian).convert("L")).astype("int64")
    mask -= mask[coords[1], coords[0]]
    mask = 1 - np.clip(np.floor(np.abs(mask)) - 10, 0, 1)
    img.putalpha(Image.fromarray((mask * 255).astype(np.uint8)))
    return img