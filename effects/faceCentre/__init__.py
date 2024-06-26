from PIL import Image
import random
import numpy as np
import math as maths
import cv2

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def findFaces(img):
    img = np.array(img.convert("RGB"))[:, :, ::-1].copy()
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.4, minNeighbors=1, minSize=(1, 1)
    )
    return faces

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
    faces = findFaces(image)
    try:
        num = random.randint(0, len(faces))
        face = faces[num]
        lastImg.paste(image, (
            int(-(face[0] - (image.width / 2) + face[2] / 2)),
            int(-(face[1] - (image.height / 2) + face[3] / 2))
        ))
    except Exception as e:
        pass
    return lastImg