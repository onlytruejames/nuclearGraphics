from PIL import Image
import numpy as np

def variables(dims, clb):
    global lastImg
    lastImg = np.array(Image.new("RGBA", dims)).astype(np.int64)

def changeDims(dims):
    global lastImg
    lastImg = np.array(Image.fromarray(lastImg.astype(np.uint8)).resize(dims)).astype(np.int64)

def callback(img):
    global lastImg
    img = np.array(img).astype(np.int64)
    img = np.maximum(img, np.roll(lastImg, (0, 1), (0, 1)))
    img = np.maximum(img, np.roll(lastImg, (0, -1), (0, 1)))
    img = np.maximum(img, np.roll(lastImg, (1, 0), (0, 1)))
    img = np.maximum(img, np.roll(lastImg, (-1, 0), (0, 1)))
    img = np.maximum(img, np.roll(lastImg, (1, 1), (0, 1)) * 0.5)
    img = np.maximum(img, np.roll(lastImg, (-1, -1), (0, 1)) * 0.5)
    img = np.maximum(img, np.roll(lastImg, (1, -1), (0, 1)) * 0.5)
    img = np.maximum(img, np.roll(lastImg, (-1, 1), (0, 1)) * 0.5)
    img = np.clip((img - 10), 0, 255)
    lastImg = img
    return Image.fromarray(img.astype(np.uint8))