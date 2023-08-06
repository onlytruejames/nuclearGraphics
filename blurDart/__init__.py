from random import randint
from PIL import (
    Image,
    ImageFilter
)

global lastImg
lastImg = Image.new("RGB", (200, 200))
gaussian = ImageFilter.GaussianBlur(radius = 10)
unsharp = ImageFilter.UnsharpMask(radius = 10, percent = 1000)

def variables(dims, clb):
    global div5size
    div5size = (int(dims[0] / 5), int(dims[1] / 5))
    return []

def callback(image, variables):
    global div5size
    width, height = div5size[0], div5size[1]

    # get a fifth of the image width and turn into coordinates of start and end points
    startCoords = (
        randint(0, width * 4),
        randint(0, height * 4)
    )
    endCoords = (
        startCoords[0] + width,
        startCoords[1] + height
    )
    img = image.crop((startCoords[0], startCoords[1], endCoords[0], endCoords[1]))
    image = image.filter(gaussian)
    image = image.filter(unsharp)
    image = image.resize((
        int(img.width),
        int(img.height)
    ))
    image = Image.blend(lastImg.resize((
        int(img.width),
        int(img.height)
    )), image, 0.5)
    img = Image.blend(img, image, 0.5)
    return img