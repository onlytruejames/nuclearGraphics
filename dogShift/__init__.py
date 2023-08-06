from PIL import Image, ImageFilter
import numpy as np
import random

gauss1 = ImageFilter.GaussianBlur(radius=2)
gauss2 = ImageFilter.GaussianBlur(radius=4)

def variables(dims, clb):
    global image, i, x, y
    i = 1
    x = 0
    y = 0
    image = Image.new("RGBA", dims)
    return []

def callback(img, variables):
    global image, i, x, y
    img1 = np.array(img.filter(gauss1), dtype="int64")
    img2 = np.array(img.filter(gauss2), dtype="int64")
    img3 = np.roll(np.abs(img1 - img2), (x, y), (0, 1))
    img3 = img3 * (255 / (np.max(img3) - np.min(img3))) - np.min(img3)
    img3 = Image.fromarray(img3.astype("uint8"))
    img3 = img3.resize((int(img3.width * i), int(img3.height * i)))
    i += (random.randint(-100, 100) / 100)
    if 0.2 > i:
        i = 0.2
    if 2 < i:
        i = 2
    x += random.randint(-50, 50)
    y += random.randint(-50, 50)
    x = x % img.height
    y = y % img.width
    image.paste(img3, (
        int((img.width - img3.width) / 2),
        int((img.height - img3.height) / 2)
    ))
    return image