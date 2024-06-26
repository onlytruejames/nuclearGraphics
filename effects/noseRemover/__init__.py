from PIL import Image
import numpy as np
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


def poprow(my_array,pr):
    """ row popping in numpy arrays
    Input: my_array - NumPy array, pr: row index to pop out
    Output: [new_array,popped_row] """
    i = pr
    pop = my_array[i]
    new_array = np.vstack((my_array[:i],my_array[i+1:]))
    return [new_array,pop]

def callback(image):
    shape = image.size
    noses = findFaces(image)
    if len(noses) > 0:
        noses = [[nose[1] + 0.45 * nose[3], nose[1] + 0.65 * nose[3]] for nose in noses]
        image = np.array(image)
        gone = []
        for nose in noses:
            for n in range(int(nose[0]), int(nose[1]), 1):
                gone.append(n)
        for i in range(len(image[0])):
            it = len(image[0]) - i
            if it in gone:
                image, a = poprow(image, it)
        return Image.fromarray(image).resize(shape)
    return image