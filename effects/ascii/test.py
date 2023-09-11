from PIL import Image
from math import sin, pi, floor

halfPi = pi / 2

size = 100

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
        floor(r * 255 + 0.5),
        floor(g * 255 + 0.5),
        floor(b * 255 + 0.5)
    )

out = Image.new("RGB", (1000, 1000))

for x in range(1000):
    colour = calc(x)
    for y in range(1000):
        out.putpixel((x, y), colour)

out.save("out.png")