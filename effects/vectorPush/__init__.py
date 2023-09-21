from PIL import Image
import numpy as np
import random
import math as maths

def callback(image):
    points = [
        [random.randint(0, image.height), random.randint(0, image.width)],
        [random.randint(0, image.height), random.randint(0, image.width)]
    ]
    diffs = np.array([(points[0][1] - points[1][1]), (points[0][0] - points[1][0])])
    if diffs[1] == 0:
        diffs[1] = 1
    gradient = diffs[1] / diffs[0]
    mag = np.sqrt(diffs.dot(diffs))
    normal = diffs / mag
    c = points[0][1] - (points[1][1] * gradient)
    pushMap = np.array([
        [(abs(
            y - (x * gradient) - c
        )) * normal for x in range(image.width)]
    for y in range(image.height)])
    img = np.array(image)
    h = image.height - 1
    w = image.width - 1
    img2 = np.array([
        [img[
            int((x + pushMap[x, y][0]) % h),
            int((y + pushMap[x, y][1]) % w)
        ] for y in range(image.width)]
        for x in range(image.height)])
    return Image.fromarray(img2)