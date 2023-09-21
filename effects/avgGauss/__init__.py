from PIL import Image, ImageFilter
import numpy as np

gauss = [ImageFilter.GaussianBlur(radius=y) for y in [2, 3, 4, 5]]

def callback(image):
    imgs = np.array([np.array(image.filter(gaus)).astype(np.int64) for gaus in gauss])
    image = np.average(imgs, 0)
    image += np.abs(imgs[0] - imgs[3])
    image = image.clip(0, 255)
    return Image.fromarray(image.astype(np.uint8))