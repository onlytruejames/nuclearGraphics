from PIL import Image
import numpy as np

def variables(dims, clb):
    global lastImg
    lastImg = Image.new("RGB", dims)

def changeDims(dims):
    global lastImg
    lastImg = lastImg.resize(dims)

def callback(image):
    global lastImg
    img = np.abs(np.array(image).astype("int64") - np.array(lastImg).astype("int64"))
    lastImg = image
    return Image.fromarray(img.astype("uint8"))