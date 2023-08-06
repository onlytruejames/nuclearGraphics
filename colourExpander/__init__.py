from PIL import Image, ImageEnhance
import numpy as np

def variables(cam, clb):
    return []

def callback(img, variables):
    img = np.array(img).astype(np.int64)
    min = np.min(img)
    max = np.max(img)
    img = img * (255 / (max+1 - min)) - min
    return ImageEnhance.Color(Image.fromarray(img.astype(np.uint8))).enhance(3)