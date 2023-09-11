from PIL import Image
from face_lib import face_lib
import random
import numpy as np
import math as maths

fl = face_lib()

global lastImg, direction
lastImg = Image.new("RGB", (200, 200))
direction = [1, 1]

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def variables(dims, clb):
    global lastImg, direction
    lastImg = Image.new("RGBA", dims, (0, 0, 0, 0))
    direction = [1, 1]

def changeDims(dims):
    global lastImg
    lastImg = lastImg.resize(dims)

def callback(image):
    global lastImg, direction
    direction = [
        direction[0] / maths.sqrt(direction[0] ** 2 + direction[1] ** 2),
        direction[1] / maths.sqrt(direction[0] ** 2 + direction[1] ** 2)
    ]
    lastImg = np.array(lastImg).astype("int64")
    lastImg -= np.array([0, 0, 0, 5])
    lastImg = np.clip(lastImg, 0, 255).astype("uint8")
    lastImg = np.roll(lastImg, (
        int(direction[0] * 30),
        int(direction[1] * 30)
    ), axis = (0, 1))
    lastImg = Image.fromarray(lastImg)
    open_cv_image = np.array(image.convert("RGB")) 
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    no_of_faces, faceCoors = fl.faces_locations(open_cv_image)
    try:
        num = random.randint(0, no_of_faces - 1)
        face = Image.fromarray(fl.get_faces(open_cv_image)[num])
        direction = [
            -(((faceCoors[num][1] * 2 + faceCoors[num][3]) - image.height) / 2) / image.height,
            (((faceCoors[num][0] * 2 + faceCoors[num][2]) - image.width) / 2) / image.width
        ]
        lastImg.paste(face, (
            int((lastImg.width / 2) - (face.width / 2)),
            int((lastImg.height / 2) - (face.height / 2)),
            int((lastImg.width / 2) + (face.width / 2)),
            int((lastImg.height / 2) + (face.height / 2)) 
        ))
    except Exception as e:
        pass
    return lastImg