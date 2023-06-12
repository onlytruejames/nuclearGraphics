from PIL import Image
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB
from random import randint

global lastImg, velocity, decay

velocity = (0, 0)
decay = 0.9

def variables(cam, clb):
    width, height = int(cam.get(3)), int(cam.get(4))
    global lastImg
    lastImg = Image.new("RGBA", (width, height))
    transparent = Image.new("RGBA", (width, height))
    return [transparent]

def callback(image, variables):
    global lastImg, velocity, decay
    transparent = variables[0]
    image = image.convert("RGBA")
    transparent.paste(lastImg, box=velocity)
    image = Image.blend(image, transparent, decay)
    lastImg = image
    velocity = (
        velocity[0] + randint(-1, 1),
        velocity[1] + randint(-1, 1)
    )
    decay += randint(-1, 1) / 10
    if decay < 0:
        decay = 0.2
    if decay > 1:
        decay = 0.9
    return image