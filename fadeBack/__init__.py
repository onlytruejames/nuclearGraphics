from PIL import Image
import numpy as np

def variables(dims, clb):
    global lastImg, baseImg
    lastImg = Image.new("RGBA", dims, (0, 0, 0, 0))
    baseImg = Image.new("RGBA", dims, (0, 0, 0, 0))

def changeDims(dims):
    global lastImg, baseImg
    lastImg = lastImg.resize(dims)
    baseImg = Image.new("RGBA", dims, (0, 0, 0, 0))

def callback(img):
    global lastImg
    lastImg = lastImg.resize((lastImg.width - 4, lastImg.height - 4))
    base = baseImg.copy()
    base.paste(lastImg, (2, 2))
    lastImg = Image.alpha_composite(base, img)
    return lastImg