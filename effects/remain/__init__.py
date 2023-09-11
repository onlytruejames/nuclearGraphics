# in memory of the uk's eu membership AMIRITE???

from PIL import Image
import numpy as np

def variables(dims, clb):
    global lastImg
    lastImg = Image.new("RGBA", dims, (0, 0, 0, 0))

def changeDims(dims):
    global lastImg
    lastImg = lastImg.resize(dims)

def callback(img):
    global lastImg
    alpha = np.array(lastImg.getchannel("A")).astype(np.int16) - 5
    alpha = Image.fromarray(alpha.clip(0, 255).astype(np.uint8))
    lastImg.putalpha(alpha)
    lastImg = Image.alpha_composite(lastImg, img)
    return lastImg