from PIL import Image
import numpy as np
from random import randint

def variables(dims, clb):
    global lastImg, lastFrame, offset
    lastImg = np.array(Image.new("RGBA", dims)).astype(np.int64)
    lastFrame = np.array(Image.new("RGBA", dims)).astype(np.int64)
    offset = np.array([0, 0])

def changeDims(dims):
    global lastImg, lastFrame
    lastImg = np.array(Image.fromarray(lastImg.astype(np.uint8)).resize(dims)).astype(np.int64)
    lastFrame = np.array(Image.fromarray(lastFrame.astype(np.uint8)).resize(dims)).astype(np.int64)

def callback(image):
    global lastImg, lastFrame, offset
    image = np.array(image).astype(np.int64)
    lastFrame = np.roll(lastFrame, offset, (0, 1))
    offset += np.array([randint(-1, 1), randint(-1, 1)])
    diff = image - lastImg
    lastFrame = np.clip(lastFrame + diff, 0, 255)
    lastImg = image
    image = lastFrame
    image = np.floor_divide(lastFrame + image, 2)
    image = Image.fromarray(image.astype(np.uint8))
    return image