from PIL import Image, ImageFilter
import numpy as np

gauss1 = ImageFilter.GaussianBlur(radius=2)
gauss2 = ImageFilter.GaussianBlur(radius=4)

def variables(dims, clb):
    global image
    image = Image.new("RGBA", dims, (0, 0, 0, 0))

def changeDims(dims):
    global image
    image = image.resize(dims)

def callback(img):
    global image
    img1 = np.array(img.filter(gauss1), dtype="int64")
    img2 = np.array(img.filter(gauss2), dtype="int64")
    img3 = np.floor_divide(np.sum(np.abs(img1 - img2), axis=2) + 225, 255)
    img = np.expand_dims(img3, 2) * np.array(img, dtype="int64")
    alpha = np.full(img3.shape, 255, dtype="int64") * img3
    img = Image.fromarray(img.astype("uint8"))
    img.putalpha(Image.fromarray(alpha.astype("uint8"), mode="L"))
    image.alpha_composite(img)
    #img = image.convert("RGB")
    image = image.filter(gauss1)
    return img