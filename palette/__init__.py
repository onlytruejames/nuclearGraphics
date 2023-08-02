from PIL import Image
from json import load
import numpy as np

global palette, palettes, val
palette = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0)
]

palettes = load(open("palette/set.json"))
print(palettes)

val = 0

def variables(cam, clb):
    clb = str(clb)
    global palette
    if clb in palettes:
        palette = palettes[clb]
    else:
        palette = [
        [0, 0, 255],
        [255, 0, 255],
        [0, 0, 255]
    ]
    return []

def callback(img, variables):
    global val
    p_img = Image.new('P', (16, 16))
    lenPaletteSector = int(256 / len(palette))
    newPal = [item for sublist in palette for item in sublist * lenPaletteSector]
    for i in range(int((768 - len(newPal)) / 3)):
        newPal.append(palette[0][0])
        newPal.append(palette[0][1])
        newPal.append(palette[0][2])
    p_img.putpalette(newPal)
    img = np.array(img.convert("L"), dtype="int64") + val
    img = Image.fromarray(np.mod(img, 255).astype("uint8"))
    val += 10
    return img.quantize(palette=p_img)