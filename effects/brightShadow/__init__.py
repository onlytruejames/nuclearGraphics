from PIL import Image
import numpy as np
from random import choice

# [
#   [1, 0, 0],
#   [0, 1, 0],
#   [0, 0, 1]
# ]
# higher values have influence over the rest of that row/column eg:
# [
#   [1, 0.5, 0],
#   [0, 1, 0.5],
#   [0, 0, 1]
# ]

def callback(image):
    isRot = choice([False, True, True, True])
    rots = {
        90: Image.ROTATE_90,
        180: Image.ROTATE_180,
        270: Image.ROTATE_270
    }
    if isRot:
        rotation = choice([90, 180, 270])
        image = image.transpose(rots[rotation])
    image = np.array(image)
    for row in range(len(image)):
        image[row] = np.maximum(image[row], image[row - 1] * 0.925)
    image = Image.fromarray(image)
    if isRot:
        image = image.transpose(rots[360 - rotation])
    return image