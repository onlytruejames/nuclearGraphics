from PIL import Image
import numpy as np

def variables(dims, clb):
    return []

def callback(image, variables):
    image = image.resize((int(image.width / 10), int(image.height / 10))).resize(image.size, 4)
    return image