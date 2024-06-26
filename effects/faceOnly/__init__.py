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

def cropFace(img, face):
    return img.crop((
        face[0],
        face[1],
        face[2] + face[0],
        face[3] + face[1]
    ))

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
    faces = findFaces(image)
    try:
        num = random.randint(0, len(faces))
        face = faces[num]
        faceImg = cropFace(image, face)
        direction = [
            -(((face[1] * 2 + face[3]) - image.height) / 2) / image.height,
            (((face[0] * 2 + face[2]) - image.width) / 2) / image.width
        ]
        lastImg.paste(faceImg, (
            int((lastImg.width / 2) - (faceImg.width / 2)),
            int((lastImg.height / 2) - (faceImg.height / 2)),
            int((lastImg.width / 2) + (faceImg.width / 2)),
            int((lastImg.height / 2) + (faceImg.height / 2)) 
        ))
    except Exception as e:
        pass
    return lastImg