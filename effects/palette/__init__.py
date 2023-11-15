from PIL import Image
import numpy as np

global val, palettes

palettes = {}
val = 0

def callback(img, palette=None):
    if palette==None:
        palette = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0)
        ]
    global val, palettes
    key = str(palette)
    if not key in palettes:
        p_img = Image.new('P', (16, 16))
        lenPaletteSector = int(256 / len(palette))
        newPal = [item for sublist in palette for item in sublist * lenPaletteSector]
        for i in range(int((768 - len(newPal)) / 3)):
            newPal.append(palette[0][0])
            newPal.append(palette[0][1])
            newPal.append(palette[0][2])
        p_img.putpalette(newPal)
        palettes[key] = p_img
    p_img = palettes[key]
    img = np.array(img.convert("L"), dtype="int64") + val
    img = Image.fromarray(np.mod(img, 255).astype("uint8"))
    val += 10
    return img.quantize(palette=p_img)