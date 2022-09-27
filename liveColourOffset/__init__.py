from PIL import Image
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB
from random import randint

global rOffset, gOffset, bOffset
rOffset = (5, 0)
gOffset = (0, 5)
bOffset = (0, 0)

def variables(cam):
    width = int(cam.get(3))
    height = int(cam.get(4))
    baked = Image.new("RGB", (width, height))
    return [baked]

def callback(cam, variables):
    global rOffset, gOffset, bOffset
    result, image = cam.read()
    baked = variables[0]
    if result:
        image = cvtColor(image, COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = image.split()
        r = baked.copy()
        r.paste(image[0], box=rOffset)
        r = r.split()[0]
        g = baked.copy()
        g.paste(image[1], box=gOffset)
        g = g.split()[1]
        b = baked.copy()
        b.paste(image[2], box=bOffset)
        b = b.split()[2]
        image = Image.merge("RGB", (r, g, b))
        rOffset = (
            rOffset[0] + randint(-1, 1),
            rOffset[1] + randint(-1, 1)
        )
        gOffset = (
            gOffset[0] + randint(-1, 1),
            gOffset[1] + randint(-1, 1)
        )
        bOffset = (
            bOffset[0] + randint(-1, 1),
            bOffset[1] + randint(-1, 1)
        )
        return image