from math import sin, pi
from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

COMMON_MONO_FONTFILENAMES = [
    'DejaVuSansMono.ttf',
    'Consolas Mono.ttf',
    'Consola.ttf'
]

def variables(dims, clb):
    global font, imageHeight, imageWidth, newHeight, newWidth
    font = None
    for fontFilename in COMMON_MONO_FONTFILENAMES:
        try:
            font = ImageFont.truetype(fontFilename, size=20)
            break
        except IOError:
            print(f'Could not load font "{fontFilename}".')
    if font is None:
        font = ImageFont.load_default()
    width, height = dims
    newWidth = int(width / 8)
    newHeight = int(height / 8)
    imageHeight, imageWidth = (int(width * 1.5), int(height * 2))

    #font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    #tallest_line = max(ASCII_CHARS, key=lambda line: font.getsize(line)[1])
    #max_line_height = font_points_to_pixels(font.getsize(tallest_line)[1])
    #realistic_line_height = max_line_height * 0.8
    #imageHeight = int(realistic_line_height * newHeight) + 1

class ImageToAscii:
    #adapted from the library image_to_ascii, which printed the output and if you wanted it to you could save it to a file, so i changed bits of it
    def __init__(self, image) -> str:
        self.image = image
        self.new_image_data = self.pixelsToAscii(self.converToGrayscale(self.image.resize((newWidth, newHeight))))
        self.asciiImage = tuple([self.new_image_data[index:(index + newWidth)] for index in range(0, newHeight * newWidth, newWidth)])
        
    def resizeImage(self,image):
        return image.resize((newWidth, newHeight))

    def converToGrayscale(self,image):
        grayscale_image = image.convert("L")
        return(grayscale_image)
        
    def pixelsToAscii(self,image):
        pixels = image.getdata()
        characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
        return(characters)    

iter = 0

halfPi = pi / 2

size = 250

def calc(x):
    x = x % size
    r = 0
    g = 0
    b = 0
    if x < size / 3:
        r = (sin((x / (size / 3 / pi * 2)) + halfPi))
        g = (sin(x / (size / 3 / pi * 2)))
    elif x < size / 3 * 2:
        g = (sin(((x - size / 3) / (size / 3 / pi * 2)) + halfPi))
        b = (sin((x - size / 3) / (size / 3 / pi * 2)))
    else:
        b = (sin(((x - size / 3 * 2) / (size / 3 / pi * 2)) + halfPi))
        r = (sin((x - size / 3 * 2) / (size / 3 / pi * 2)))
    return (
        int(r * 255 + 0.5),
        int(g * 255 + 0.5),
        int(b * 255 + 0.5)
    )

colours = [calc(x) for x in range(size)]

def textfile_to_image(lines):
    # stolen from stackoverflow
    # make a sufficiently sized background image based on the combination of font and lines

    # draw the background

    global iter
    backgroundColour = colours[iter % size]

    image = Image.new("RGB", (imageWidth, imageHeight), color=backgroundColour)
    draw = ImageDraw.Draw(image)

    # draw each line of text
    fontColour = calc((iter + size / 2) % size)

    for i, line in enumerate(lines):
        vertical_position = int(round(i * 17))
        draw.text((0, vertical_position), line, fill=fontColour, font=font)

    return image

def callback(img):
    global font, imageHeight, imageWidth, newHeight, newWidth
    img = textfile_to_image(ImageToAscii(img).asciiImage).resize(img.size)
    global iter
    iter += 1
    return img