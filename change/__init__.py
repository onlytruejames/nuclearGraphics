from PIL import Image
import numpy as np

def variables(dims, clb):
    global lastImg
    lastImg = Image.new("RGB", dims)

def changeDims(dims):
    global lastImg
    lastImg = lastImg.resize(dims)

def callback(image):
    alpha = image.getchannel("A")
    image = image.convert("RGB")
    global lastImg
    img = np.abs(np.array(image).astype("int64") - np.array(lastImg).astype("int64"))
    lastImg = image
    image = Image.fromarray(img.astype("uint8"))
    image.putalpha(alpha)
    return image