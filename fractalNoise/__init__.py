from PIL import Image
import numpy as np
import noise, random

fractal = np.array([noise.pnoise3(x * 10 + 0.01, y * 10 + 0.01, z * 10 + 0.01) for x in range(100) for y in range(100) for z in range(100)]) + 1
fractal += (np.array([noise.pnoise3(x * 100 + 0.01, y * 100 + 0.01, z * 100 + 0.01) for x in range(100) for y in range(100) for z in range(100)]) + 1) * 0.6
fractal += (np.array([noise.pnoise3(x / 10 + 0.01, y / 10 + 0.01, z / 10 + 0.01) for x in range(100) for y in range(100) for z in range(100)]) + 1) * 0.4
fractal += (np.array([noise.pnoise3(x + 0.01, y + 0.01, z + 0.01) for x in range(100) for y in range(100) for z in range(100)]) + 1) * 0.2
fractal = (np.divide(fractal, 2.2) * 127).astype("uint8")
fractal = fractal.reshape((100, 100, 100))

def variables(cam, clb):
    global bg
    bg = Image.new("RGBA", (cam.get(3), cam.get(4)), (0, 0, 0, 255))
    return []

def callback(img, variables):
    global bg
    match random.randint(1, 3):
        case 1:
            fracSlice = fractal[0:99, 0:99, random.randint(0, 99)]
        case 2:
            fracSlice = fractal[0:99, random.randint(0, 99), 0:99]
        case 3:
            fracSlice = fractal[random.randint(0, 99), 0:99, 0:99]
    img.putalpha(Image.fromarray(fracSlice).resize(img.size))
    return Image.alpha_composite(bg, img)