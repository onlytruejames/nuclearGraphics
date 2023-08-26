from PIL import Image, ImageFilter
import numpy as np
import random

gaussian = ImageFilter.GaussianBlur()

def variables(dims, clb):
    return []

def callback(img, variables):
    coords = (random.randint(0, img.width - 1), random.randint(0, img.height - 1))
    mask = np.array(img.filter(gaussian).convert("L")).astype("int64")
    img = np.array(img)
    mask -= mask[coords[1], coords[0]]
    mask = np.clip(np.floor(np.abs(mask)) - 10, 0, 1)
    return Image.fromarray(img * np.expand_dims(mask.astype("uint8"), 2))