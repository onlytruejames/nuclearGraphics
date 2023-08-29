from PIL import Image
from face_lib import face_lib
import random
import numpy as np
import math as maths

fl = face_lib()

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def variables(dims, clb):
    global lastImg
    lastImg = Image.new("RGBA", dims, (0, 0, 0, 0))

def changeDims(dims):
    global lastImg
    lastImg = lastImg.resize(dims)

def callback(image):
    global lastImg
    lastImg = np.array(lastImg).astype("int64")
    lastImg -= np.array([0, 0, 0, 20])
    lastImg = np.clip(lastImg, 0, 255).astype("uint8")
    lastImg = Image.fromarray(lastImg)
    open_cv_image = np.array(image.convert("RGB")) 
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    no_of_faces, faceCoors = fl.faces_locations(open_cv_image)
    try:
        num = random.randint(0, no_of_faces - 1)
        lastImg.paste(image, (
            int(-(faceCoors[num][0] - (image.width / 2) + faceCoors[num][2] / 2)),
            int(-(faceCoors[num][1] - (image.height / 2) + faceCoors[num][3] / 2))
        ))
    except Exception as e:
        pass
    return lastImg